from util.number_utils import ip_to_num, add_ip
from stats.defense.regress_defense import regress_defensive_stats
from output_utils.progress.progress_bar import ProgressBar

def calculate_defensive_stats(tourney_data, cards):
    positions = ["C", "1B", "2B", "3B", "SS", "LF", "CF", "RF"]

    position_players_data = {
        "C": {},
        "1B": {},
        "2B": {},
        "3B": {},
        "SS": {},
        "LF": {},
        "CF": {},
        "RF": {}
    }
    position_biz_breakdown = {
        "C": { "totbiz": 0, "routinebiz": 0, "likelybiz": 0, "evenbiz": 0, "unlikelybiz": 0, "veryunlikelybiz": 0, "routinebizfield": 0, "likelybizfield": 0, "evenbizfield": 0, "unlikelybizfield": 0, "veryunlikelybizfield": 0 },
        "1B": { "totbiz": 0, "routinebiz": 0, "likelybiz": 0, "evenbiz": 0, "unlikelybiz": 0, "veryunlikelybiz": 0, "routinebizfield": 0, "likelybizfield": 0, "evenbizfield": 0, "unlikelybizfield": 0, "veryunlikelybizfield": 0 },
        "2B": { "totbiz": 0, "routinebiz": 0, "likelybiz": 0, "evenbiz": 0, "unlikelybiz": 0, "veryunlikelybiz": 0, "routinebizfield": 0, "likelybizfield": 0, "evenbizfield": 0, "unlikelybizfield": 0, "veryunlikelybizfield": 0 },
        "3B": { "totbiz": 0, "routinebiz": 0, "likelybiz": 0, "evenbiz": 0, "unlikelybiz": 0, "veryunlikelybiz": 0, "routinebizfield": 0, "likelybizfield": 0, "evenbizfield": 0, "unlikelybizfield": 0, "veryunlikelybizfield": 0 },
        "SS": { "totbiz": 0, "routinebiz": 0, "likelybiz": 0, "evenbiz": 0, "unlikelybiz": 0, "veryunlikelybiz": 0, "routinebizfield": 0, "likelybizfield": 0, "evenbizfield": 0, "unlikelybizfield": 0, "veryunlikelybizfield": 0 },
        "LF": { "totbiz": 0, "routinebiz": 0, "likelybiz": 0, "evenbiz": 0, "unlikelybiz": 0, "veryunlikelybiz": 0, "routinebizfield": 0, "likelybizfield": 0, "evenbizfield": 0, "unlikelybizfield": 0, "veryunlikelybizfield": 0 },
        "CF": { "totbiz": 0, "routinebiz": 0, "likelybiz": 0, "evenbiz": 0, "unlikelybiz": 0, "veryunlikelybiz": 0, "routinebizfield": 0, "likelybizfield": 0, "evenbizfield": 0, "unlikelybizfield": 0, "veryunlikelybizfield": 0 },
        "RF": { "totbiz": 0, "routinebiz": 0, "likelybiz": 0, "evenbiz": 0, "unlikelybiz": 0, "veryunlikelybiz": 0, "routinebizfield": 0, "likelybizfield": 0, "evenbizfield": 0, "unlikelybizfield": 0, "veryunlikelybizfield": 0 }
    }
    total_fielding_ip_per_pos = {}

    # Use these to calculate avg play%
    tot_biz_per_pos = {
        "C": 0,
        "1B": 0,
        "2B": 0,
        "3B": 0,
        "SS": 0,
        "LF": 0,
        "CF": 0,
        "RF": 0
    }
    tot_fieldedbiz_per_pos = {
        "C": 0,
        "1B": 0,
        "2B": 0,
        "3B": 0,
        "SS": 0,
        "LF": 0,
        "CF": 0,
        "RF": 0
    }

    # Used to calculate outputs
    regression_data = {
        "C": {},
        "1B": {},
        "2B": {},
        "3B": {},
        "SS": {},
        "LF": {},
        "CF": {},
        "RF": {}
    }
    r2_data = {
        "C": {},
        "1B": {},
        "2B": {},
        "3B": {},
        "SS": {},
        "LF": {},
        "CF": {},
        "RF": {}
    }

    progress_bar = ProgressBar(len(tourney_data.keys()), "Reading tourney players for fielding data")
    
    for (key, pi) in tourney_data.items():
        progress_bar.increment()
        player_positions = 0
        for position in positions:
            if pi[position.lower() + "x"] > 0:
                player_positions += 1
        if player_positions > 1:
            continue
        if pi["pos"] not in position_players_data:
            continue
        tot_biz_per_pos[pi["pos"]] += pi["totalbiz"]
        tot_fieldedbiz_per_pos[pi["pos"]] += pi["totalplaysfielded"]

        position_biz_breakdown[pi["pos"]]["totbiz"] += pi["totalbiz"]
        position_biz_breakdown[pi["pos"]]["routinebiz"] += pi["routinebiz"]
        position_biz_breakdown[pi["pos"]]["likelybiz"] += pi["likelybiz"]
        position_biz_breakdown[pi["pos"]]["evenbiz"] += pi["evenbiz"]
        position_biz_breakdown[pi["pos"]]["unlikelybiz"] += pi["unlikelybiz"]
        position_biz_breakdown[pi["pos"]]["veryunlikelybiz"] += pi["veryunlikelybiz"]

        position_biz_breakdown[pi["pos"]]["routinebizfield"] += pi["routinebizfield"]
        position_biz_breakdown[pi["pos"]]["likelybizfield"] += pi["likelybizfield"]
        position_biz_breakdown[pi["pos"]]["evenbizfield"] += pi["evenbizfield"]
        position_biz_breakdown[pi["pos"]]["unlikelybizfield"] += pi["unlikelybizfield"]
        position_biz_breakdown[pi["pos"]]["veryunlikelybizfield"] += pi["veryunlikelybizfield"]

        if pi["pos"] not in total_fielding_ip_per_pos:
            total_fielding_ip_per_pos[pi["pos"]] = 0
        total_fielding_ip_per_pos[pi["pos"]] = add_ip(pi["fieldingip"], total_fielding_ip_per_pos[pi["pos"]])
        position_players_data[pi["pos"]][key] = pi
    progress_bar.finish()

    for position in position_biz_breakdown:
        for key in position_biz_breakdown[position]:
            # Per game stats
            position_biz_breakdown[position][key] = position_biz_breakdown[position][key] / ip_to_num(total_fielding_ip_per_pos[position]) * 9
    
    position_info = [
        ("C", [
            ("adj_play_pct", [
                "carm", 
                "cabi"
            ]),
            ("adj_zr", [
                "carm", 
                "cabi"
            ]),
            ("adj_totbiz", [
                "ifrng"
            ])
        ]),
        ("1B", [
            ("adj_play_pct", [
                "ifrng", 
                "ifarm",  
                "iferr", 
                "tdp",
                "height"
            ]),
            ("adj_zr", [
                "ifrng", 
                "ifarm",  
                "iferr", 
                "tdp",
                "height"
            ]),
            ("adj_totbiz", [
                "ifrng"
            ])
        ]),
        ("2B", [
            ("adj_play_pct", [
                "ifrng", 
                "ifarm",  
                "iferr", 
                "tdp"
            ]),
            ("adj_zr", [
                "ifrng", 
                "ifarm",  
                "iferr", 
                "tdp"
            ]),
            ("adj_totbiz", [
                "ifrng"
            ])
        ]),
        ("3B", [
            ("adj_play_pct", [
                "ifrng", 
                "ifarm",  
                "iferr", 
                "tdp"
            ]),
            ("adj_zr", [
                "ifrng", 
                "ifarm",  
                "iferr", 
                "tdp"
            ]),
            ("adj_totbiz", [
                "ifrng"
            ])
        ]),
        ("SS", [
            ("adj_play_pct", [
                "ifrng", 
                "ifarm",  
                "iferr", 
                "tdp"
            ]),
            ("adj_zr", [
                "ifrng", 
                "ifarm",  
                "iferr", 
                "tdp"
            ]),
            ("adj_totbiz", [
                "ifrng"
            ])
        ]),
        ("LF", [
            ("adj_play_pct", [
                "ofrng", 
                "ofarm", 
                "oferr"
            ]),
            ("adj_zr", [
                "ofrng", 
                "ofarm", 
                "oferr"
            ]),
            ("adj_totbiz", [
                "ofrng"
            ])
        ]),
        ("CF", [
            ("adj_play_pct", [
                "ofrng", 
                "ofarm", 
                "oferr"
            ]),
            ("adj_zr", [
                "ofrng", 
                "ofarm", 
                "oferr"
            ]),
            ("adj_totbiz", [
                "ofrng"
            ])
        ]),
        ("RF", [
            ("adj_play_pct", [
                "ofrng", 
                "ofarm", 
                "oferr"
            ]),
            ("adj_zr", [
                "ofrng", 
                "ofarm", 
                "oferr"
            ]),
            ("adj_totbiz", [
                "ofrng"
            ])
        ])
    ]

    progress_bar = ProgressBar(len(position_info) * len(position_info[0][1]), "Calculating fielding regressions")
    for position, pos_regs in position_info:
        _calculate_normalized_play_pct(position_players_data[position], position_biz_breakdown[position])
        for (outcome_stat, pos_ratings) in pos_regs:
            reg, r2 = regress_defensive_stats(position_players_data[position], pos_ratings, outcome_stat)
            regression_data[position][outcome_stat] = reg
            r2_data[position][outcome_stat] = r2

            progress_bar.increment()
    progress_bar.finish()

    for position in r2_data.keys():
        for outcome_stat in r2_data[position].keys():
            print(position, outcome_stat, "r2:", r2_data[position][outcome_stat])
    print()

    outs_above_average_per_162 = {}
    zr_per_162 = {}
    for position in regression_data.keys():
        outs_above_average_per_162[position] = _get_oaa_fn(position, regression_data, position_biz_breakdown)
        zr_per_162[position] = _get_zr_fn(position, regression_data)

    positions = ["C", "1B", "2B", "3B", "SS", "LF", "CF", "RF"]
    progress_bar = ProgressBar(len(cards), "Calculate in defensive stats to cards")
    for card in cards:
        for position in positions:
            card[position + "_expected_zr"] = zr_per_162[position](card)
            card[position + "_expected_outs_above_avg"] = outs_above_average_per_162[position](card)
        progress_bar.increment()
    progress_bar.finish()

def _get_oaa_fn(position, regression_data, position_biz_breakdown):
    avg_play_pct = (position_biz_breakdown[position]["routinebizfield"] + position_biz_breakdown[position]["likelybizfield"] + position_biz_breakdown[position]["evenbizfield"] 
        + position_biz_breakdown[position]["unlikelybizfield"] + position_biz_breakdown[position]["veryunlikelybizfield"]) / position_biz_breakdown[position]["totbiz"]
    avg_totbiz_per_year = position_biz_breakdown[position]["totbiz"] * 162

    outs_per_year = avg_totbiz_per_year * avg_play_pct

    play_pct_regression = regression_data[position]["adj_play_pct"]
    totbiz_regression = regression_data[position]["adj_totbiz"]

    get_tot_biz = None
    get_play_pct = None
    if position == "C":
        get_tot_biz = lambda pi: totbiz_regression[0] + totbiz_regression[1] * pi["ifrng"]
        get_play_pct = lambda pi: play_pct_regression[0] + play_pct_regression[1] * pi["carm"] + play_pct_regression[2] * pi["cabi"]
    elif position == "1B":
        get_tot_biz = lambda pi: totbiz_regression[0] + totbiz_regression[1] * pi["ifrng"]
        get_play_pct = lambda pi: play_pct_regression[0] + play_pct_regression[1] * pi["ifrng"] + play_pct_regression[2] * pi["ifarm"] + play_pct_regression[3] * pi["iferr"] + play_pct_regression[4] * pi["tdp"] + play_pct_regression[5] * pi["height"]
    elif position == "2B" or position == "3B" or position == "SS":
        get_tot_biz = lambda pi: totbiz_regression[0] + totbiz_regression[1] * pi["ifrng"]
        get_play_pct = lambda pi: play_pct_regression[0] + play_pct_regression[1] * pi["ifrng"] + play_pct_regression[2] * pi["ifarm"] + play_pct_regression[3] * pi["iferr"] + play_pct_regression[4] * pi["tdp"]
    elif position == "LF" or position == "CF" or position == "RF":
        get_tot_biz = lambda pi: totbiz_regression[0] + totbiz_regression[1] * pi["ofrng"]
        get_play_pct = lambda pi: play_pct_regression[0] + play_pct_regression[1] * pi["ofrng"] + play_pct_regression[2] * pi["ofarm"] + play_pct_regression[3] * pi["oferr"]

    return lambda pi: get_tot_biz(pi) * get_play_pct(pi) - outs_per_year

def _get_zr_fn(position, regression_data):
    zr_reg = regression_data[position]["adj_zr"]
    if position == "C":
        return lambda pi: zr_reg[0] + zr_reg[1] * pi["carm"] + zr_reg[2] * pi["cabi"]
    elif position == "1B":
        return lambda pi: zr_reg[0] + zr_reg[1] * pi["ifrng"] + zr_reg[2] * pi["ifarm"] + zr_reg[3] * pi["iferr"] + zr_reg[4] * pi["tdp"] + zr_reg[5] * pi["height"]
    elif position == "2B" or position == "3B" or position == "SS":
        return lambda pi: zr_reg[0] + zr_reg[1] * pi["ifrng"] + zr_reg[2] * pi["ifarm"] + zr_reg[3] * pi["iferr"] + zr_reg[4] * pi["tdp"]
    elif position == "LF" or position == "CF" or position == "RF":
        return lambda pi: zr_reg[0] + zr_reg[1] * pi["ofrng"] + zr_reg[2] * pi["ofarm"] + zr_reg[3] * pi["oferr"]

def _calculate_normalized_play_pct(positon_players, normalized_data):
    for player in positon_players.values():
        rbiz_successes = player["routinebizfield"] / player["routinebiz"] * normalized_data["routinebiz"] if player["routinebiz"] > 0 else 0
        lbiz_successes = player["likelybizfield"] / player["likelybiz"] * normalized_data["likelybiz"] if player["likelybiz"] > 0 else 0
        ebiz_successes = player["evenbizfield"] / player["evenbiz"] * normalized_data["evenbiz"] if player["evenbiz"] > 0 else 0
        ulbiz_successes = player["unlikelybizfield"] / player["unlikelybiz"] * normalized_data["unlikelybiz"] if player["unlikelybiz"] > 0 else 0
        vulbiz_successes = player["veryunlikelybizfield"] / player["veryunlikelybiz"] * normalized_data["veryunlikelybiz"] if player["veryunlikelybiz"] > 0 else 0
        player["adj_play_pct"] = (rbiz_successes + lbiz_successes + ebiz_successes + ulbiz_successes + vulbiz_successes) / normalized_data["totbiz"] if normalized_data["totbiz"] > 0 else 0

        player["adj_fieldedballs"] = (player["routinebizfield"] + player["likelybizfield"] + player["evenbizfield"] + player["unlikelybizfield"] 
            + player["veryunlikelybizfield"]) / ip_to_num(player["fieldingip"]) * 9 * 162 if player["fieldingip"] > 0 else 0

        player["adj_totbiz"] = player["totalbiz"] / ip_to_num(player["fieldingip"]) * 9 * 162 if player["fieldingip"] > 0 else 0

        player["adj_zr"] = player["zr"] / ip_to_num(player["fieldingip"]) * 9 * 162 if player["fieldingip"] > 0 else 0