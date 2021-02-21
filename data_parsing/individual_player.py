from util.number_utils import add_ip, ip_to_num, int_or_zero, int_or_negative, float_or_zero

def read_individual_player(player_ratings, player_info, column_names):
    ip_index = column_names.index("IP")
    ab_index = column_names.index("AB")
    pitcher_games = int_or_zero(player_info[column_names.index("G", column_names.index("BsR"))])
    pitcher_gamesstarted = int_or_zero(player_info[column_names.index("GS", column_names.index("BsR"))])
    batter_pa = int(player_info[column_names.index("PA")])

    # Throw out players with no data
    # If the player was both a starter and reliever in a single season, don't waste time trying to parse out data
    player_type = None
    if pitcher_games > 0 and pitcher_gamesstarted == 0:
        player_type = "reliever"
    elif pitcher_games > 0 and pitcher_gamesstarted == pitcher_games:
        player_type = "starter"
    elif batter_pa > 0:
        player_type = "batter"

    if player_type == None:
        return None

    tot_balls_in_zone = (int_or_zero(player_info[column_names.index("BIZ-R")]) + int_or_zero(player_info[column_names.index("BIZ-L")]) 
    + int_or_zero(player_info[column_names.index("BIZ-E")]) + int_or_zero(player_info[column_names.index("BIZ-U")]) + int_or_zero(player_info[column_names.index("BIZ-Z")]) 
    + int_or_zero(player_info[column_names.index("BIZ-I")]))
    tot_plays_fielded = (int_or_zero(player_info[column_names.index("BIZ-Rm")]) + int_or_zero(player_info[column_names.index("BIZ-Lm")]) 
    + int_or_zero(player_info[column_names.index("BIZ-Em")]) + int_or_zero(player_info[column_names.index("BIZ-Um")]) + int_or_zero(player_info[column_names.index("BIZ-Zm")]))
    playpct = 0
    routinefieldpct = 0
    if tot_balls_in_zone > 0:
        playpct = tot_plays_fielded / tot_balls_in_zone
        routinefieldpct = int_or_zero(player_info[column_names.index("BIZ-R")]) / tot_balls_in_zone
    
    return {
        "team": player_info[column_names.index("TM")] + player_info[column_names.index("TM") + 1],
        "pos": player_info[column_names.index("POS")],
        "bats": player_info[column_names.index("B")],
        "throws": player_info[column_names.index("T")],
        "pa": int(player_info[column_names.index("PA")]),
        "gs": int_or_zero(player_info[column_names.index("GS")]),
        "g": int_or_zero(player_info[column_names.index("G")]),
        "ab": int(player_info[ab_index]),
        "woba": float(player_info[column_names.index("wOBA")]),
        "sp_bf": _read_pitcher_data(player_type, "starter", int(player_info[column_names.index("BF")])),
        "rp_bf": _read_pitcher_data(player_type, "reliever", int(player_info[column_names.index("BF")])),
        "games": pitcher_games,
        "gamesstarted": pitcher_gamesstarted,
        "sp_fip": _read_pitcher_data(player_type, "starter", float(player_info[column_names.index("FIP")])),
        "rp_fip": _read_pitcher_data(player_type, "reliever", float(player_info[column_names.index("FIP")])),
        "sp_ip": _read_pitcher_data(player_type, "starter", float(player_info[ip_index])),
        "rp_ip": _read_pitcher_data(player_type, "reliever", float(player_info[ip_index])),
        "sp_hra": _read_pitcher_data(player_type, "starter", int(player_info[column_names.index("HR", ip_index)])),
        "rp_hra": _read_pitcher_data(player_type, "reliever", int(player_info[column_names.index("HR", ip_index)])),
        "sp_hitsallowed": _read_pitcher_data(player_type, "starter", int(player_info[column_names.index("HA", ip_index)])),
        "rp_hitsallowed": _read_pitcher_data(player_type, "reliever", int(player_info[column_names.index("HA", ip_index)])),
        "sp_k": _read_pitcher_data(player_type, "starter", int(player_info[column_names.index("K", ip_index)])),
        "rp_k": _read_pitcher_data(player_type, "reliever", int(player_info[column_names.index("K", ip_index)])),
        "sp_bb": _read_pitcher_data(player_type, "starter", int(player_info[column_names.index("BB", ip_index)])),
        "rp_bb": _read_pitcher_data(player_type, "reliever", int(player_info[column_names.index("BB", ip_index)])),
        "sp_bb_hp": _read_pitcher_data(player_type, "starter", int(player_info[column_names.index("BB", ip_index)]) + int(player_info[column_names.index("HP", column_names.index("BsR"))])),
        "rp_bb_hp": _read_pitcher_data(player_type, "reliever", int(player_info[column_names.index("BB", ip_index)]) + int(player_info[column_names.index("HP", column_names.index("BsR"))])),
        "sp_whip": _read_pitcher_data(player_type, "starter", float_or_zero(player_info[column_names.index("WHIP")])),
        "rp_whip": _read_pitcher_data(player_type, "reliever", float_or_zero(player_info[column_names.index("WHIP")])),
        "bwar": float_or_zero(player_info[column_names.index("WAR")]),
        "sp_war": _read_pitcher_data(player_type, "starter", float(player_info[column_names.index("WAR", ip_index)])),
        "rp_war": _read_pitcher_data(player_type, "reliever", float(player_info[column_names.index("WAR", ip_index)])),
        "wraa": float_or_zero(player_info[column_names.index("wRAA")]),
        "batr": float_or_zero(player_info[column_names.index("BatR")]),
        "bsrunchances": (
            int(player_info[column_names.index("1B", ab_index)])
            + int(player_info[column_names.index("2B", ab_index)])
            + int(player_info[column_names.index("3B", ab_index)])
            + int(player_info[column_names.index("BB", ab_index)])
            + int(player_info[column_names.index("HP", ab_index)])
        ),
        "stealchances": (
            int(player_info[column_names.index("1B", ab_index)])
            + int(player_info[column_names.index("2B", ab_index)])
            + int(player_info[column_names.index("BB", ab_index)])
            + int(player_info[column_names.index("HP", ab_index)])
        ),
        "sp_pitch_stealchances": _read_pitcher_data(player_type, "starter", (
            int(player_info[column_names.index("HA", ip_index)]) 
            + int(player_info[column_names.index("BB", ip_index)]) 
            + int(player_info[column_names.index("HP", column_names.index("BsR"))])
        )),
        "rp_pitch_stealchances": _read_pitcher_data(player_type, "reliever", (
            int(player_info[column_names.index("HA", ip_index)]) 
            + int(player_info[column_names.index("BB", ip_index)]) 
            + int(player_info[column_names.index("HP", column_names.index("BsR"))])
        )),
        "sp_pitch_basesstolen": _read_pitcher_data(player_type, "starter", (
            int(player_info[column_names.index("SB", ip_index)])
        )),
        "rp_pitch_basesstolen": _read_pitcher_data(player_type, "reliever", (
            int(player_info[column_names.index("SB", ip_index)])
        )),
        "sp_pitch_basesstolen_wild_pitch": _read_pitcher_data(player_type, "starter", (
            int(player_info[column_names.index("SB", ip_index)]) + int_or_zero(player_info[column_names.index("WP")])
        )),
        "rp_pitch_basesstolen_wild_pitch": _read_pitcher_data(player_type, "reliever", (
            int(player_info[column_names.index("SB", ip_index)]) + int_or_zero(player_info[column_names.index("WP")])
        )),
        "sp_pitch_stealattempts": _read_pitcher_data(player_type, "starter", (
            int(player_info[column_names.index("SB", ip_index)])
            + int(player_info[column_names.index("CS", ip_index)])
        )),
        "rp_pitch_stealattempts": _read_pitcher_data(player_type, "reliever", (
            int(player_info[column_names.index("SB", ip_index)])
            + int(player_info[column_names.index("CS", ip_index)])
        )),
        "sp_earned_runs": _read_pitcher_data(player_type, "starter", (
            int(player_info[column_names.index("ER", ip_index)])
        )),
        "rp_earned_runs": _read_pitcher_data(player_type, "reliever", (
            int(player_info[column_names.index("ER", ip_index)])
        )),
        "sp_pitch_non_hr_hits": _read_pitcher_data(player_type, "starter", (
            int(player_info[column_names.index("HA", ip_index)])
            - int(player_info[column_names.index("HR", ip_index)])
        )),
        "rp_pitch_non_hr_hits": _read_pitcher_data(player_type, "reliever", (
            int(player_info[column_names.index("HA", ip_index)])
            - int(player_info[column_names.index("HR", ip_index)])
        )),
        "sp_pitcherdoubleplays": _read_pitcher_data(player_type, "starter", (
            int(player_info[column_names.index("DP", ip_index)])
        )),
        "rp_pitcherdoubleplays": _read_pitcher_data(player_type, "reliever", (
            int(player_info[column_names.index("DP", ip_index)])
        )),
        "wsb": float(player_info[column_names.index("wSB", ab_index)]),
        "ubr": float(player_info[column_names.index("UBR", ab_index)]),
        "baserunningruns": float_or_zero(player_info[column_names.index("BsR")]),
        "zr": float(player_info[column_names.index("ZR")]),
        "fieldingip": float(player_info[column_names.index("IP", column_names.index("ZR"))]),
        # leverage is only relevant for RP
        "leverage": _read_pitcher_data(player_type, "reliever", float_or_zero(player_info[column_names.index("pLi")])),
        "strikeouts": int(player_info[column_names.index("SO")]),
        "walks": int(player_info[column_names.index("BB")]),
        "homeruns": int(player_info[column_names.index("HR")]),
        "hits": int(player_info[column_names.index("H")]),
        "doubles": int_or_zero(player_info[column_names.index("2B")]),
        "triples": int_or_zero(player_info[column_names.index("3B")]),
        "runsscored": int_or_zero(player_info[column_names.index("R")]),
        "rbi": int_or_zero(player_info[column_names.index("RBI")]),
        "intentionallywalked": int_or_zero(player_info[column_names.index("IBB")]),
        "sacflies": int_or_zero(player_info[column_names.index("SF")]),
        "sacbunts": int_or_zero(player_info[column_names.index("SH")]),
        "gidp": int_or_zero(player_info[column_names.index("GDP")]),
        "stolenbases": int_or_zero(player_info[column_names.index("SB")]),
        "caughtstealing": int_or_zero(player_info[column_names.index("CS")]),
        "routinebiz": int_or_zero(player_info[column_names.index("BIZ-R")]),
        "routinebizfield": int_or_zero(player_info[column_names.index("BIZ-Rm")]),
        "routinebizpct": int_or_zero(player_info[column_names.index("BIZ-Rm")]) / int_or_zero(player_info[column_names.index("BIZ-R")]) if int_or_zero(player_info[column_names.index("BIZ-R")]) > 0 else 0,
        "likelybiz": int_or_zero(player_info[column_names.index("BIZ-L")]),
        "likelybizfield": int_or_zero(player_info[column_names.index("BIZ-Lm")]),
        "likelybizpct": int_or_zero(player_info[column_names.index("BIZ-Lm")]) / int_or_zero(player_info[column_names.index("BIZ-L")]) if int_or_zero(player_info[column_names.index("BIZ-L")]) > 0 else 0,
        "evenbiz": int_or_zero(player_info[column_names.index("BIZ-E")]),
        "evenbizfield": int_or_zero(player_info[column_names.index("BIZ-Em")]),
        "evenbizpct": int_or_zero(player_info[column_names.index("BIZ-Rm")]) / int_or_zero(player_info[column_names.index("BIZ-E")]) if int_or_zero(player_info[column_names.index("BIZ-E")]) > 0 else 0,
        "unlikelybiz": int_or_zero(player_info[column_names.index("BIZ-U")]),
        "unlikelybizfield": int_or_zero(player_info[column_names.index("BIZ-Um")]),
        "unlikelybizpct": int_or_zero(player_info[column_names.index("BIZ-Rm")]) / int_or_zero(player_info[column_names.index("BIZ-U")]) if int_or_zero(player_info[column_names.index("BIZ-U")]) > 0 else 0,
        "veryunlikelybiz": int_or_zero(player_info[column_names.index("BIZ-Z")]),
        "veryunlikelybizfield": int_or_zero(player_info[column_names.index("BIZ-Zm")]),
        "veryunlieklybizpct": int_or_zero(player_info[column_names.index("BIZ-Rm")]) / int_or_zero(player_info[column_names.index("BIZ-Z")]) if int_or_zero(player_info[column_names.index("BIZ-Z")]) > 0 else 0,
        "impossiblebiz": int_or_zero(player_info[column_names.index("BIZ-I")]),
        "totalbiz": tot_balls_in_zone,
        "totalplaysfielded": tot_plays_fielded,
        "playpct": playpct,
        "routinefieldpct": routinefieldpct,
        "totalchances": int_or_zero(player_info[column_names.index("TC", column_names.index("FIP-"))]),
        "assists": int_or_zero(player_info[column_names.index("A", column_names.index("FIP-"))]),
        "putouts": int_or_zero(player_info[column_names.index("PO", column_names.index("FIP-"))]),
        "stolenbaseattempts": int_or_zero(player_info[column_names.index("SBA", column_names.index("ZR"))]),
        "runnersthrownout": int_or_negative(player_info[column_names.index("RTO", column_names.index("ZR"))]),
        "errors": int_or_zero(player_info[column_names.index("E", column_names.index("FIP-"))]),
        "doubleplays": int_or_zero(player_info[column_names.index("DP", column_names.index("FIP-"))]),
        "sp_playershitbypitch": _read_pitcher_data(player_type, "starter", int(player_info[column_names.index("HP", column_names.index("BsR"))])),
        "rp_playershitbypitch": _read_pitcher_data(player_type, "reliever", int(player_info[column_names.index("HP", column_names.index("BsR"))])),
        "timeshitbypitch": int(player_info[column_names.index("HP")]),
        "sp_wildpitches": _read_pitcher_data(player_type, "starter", int_or_zero(player_info[column_names.index("WP")])),
        "rp_wildpitches": _read_pitcher_data(player_type, "reliever", int_or_zero(player_info[column_names.index("WP")])),
        "cera": float_or_zero(player_info[column_names.index("CERA")]),
        "sp_era": _read_pitcher_data(player_type, "starter", float_or_zero(player_info[column_names.index("ERA")])),
        "rp_era": _read_pitcher_data(player_type, "reliever", float_or_zero(player_info[column_names.index("ERA")])),
        **player_ratings,
    }

# Ugly method. Does what it needs to do.
def merge_player_data(old_info, new_info):
    if ip_to_num(add_ip(old_info["fieldingip"], new_info["fieldingip"])) > 0:
        old_info["cera"] = (old_info["cera"] * ip_to_num(old_info["fieldingip"]) + new_info["cera"] * ip_to_num(new_info["fieldingip"])) / ip_to_num(add_ip(old_info["fieldingip"], new_info["fieldingip"]))
    if (new_info["sp_bf"] + old_info["sp_bf"] > 0):
        old_info["sp_fip"] = (new_info["sp_bf"] * new_info["sp_fip"] + old_info["sp_bf"] * old_info["sp_fip"]) / (new_info["sp_bf"] + old_info["sp_bf"])
    if (new_info["rp_bf"] + old_info["rp_bf"] > 0):
        old_info["rp_fip"] = (new_info["rp_bf"] * new_info["rp_fip"] + old_info["rp_bf"] * old_info["rp_fip"]) / (new_info["rp_bf"] + old_info["rp_bf"])
        old_info["leverage"] = (new_info["rp_bf"] * new_info["leverage"] + old_info["rp_bf"] * old_info["leverage"]) / (new_info["rp_bf"] + old_info["rp_bf"])
    if (new_info["pa"] + old_info["pa"] > 0):
        old_info["woba"] = (new_info["pa"] * new_info["woba"] + old_info["pa"] * old_info["woba"]) / (new_info["pa"] + old_info["pa"])
    if ip_to_num(add_ip(old_info["sp_ip"], new_info["sp_ip"])) > 0:
        old_info["sp_era"] = (old_info["sp_era"] * ip_to_num(old_info["sp_ip"]) + new_info["sp_era"] * ip_to_num(new_info["sp_ip"])) / ip_to_num(add_ip(old_info["sp_ip"], new_info["sp_ip"]))
        old_info["sp_whip"] = (old_info["sp_whip"] * ip_to_num(old_info["sp_ip"]) + new_info["sp_whip"] * ip_to_num(new_info["sp_ip"])) / ip_to_num(add_ip(old_info["sp_ip"], new_info["sp_ip"]))
    if ip_to_num(add_ip(old_info["rp_ip"], new_info["rp_ip"])) > 0:
        old_info["rp_era"] = (old_info["rp_era"] * ip_to_num(old_info["rp_ip"]) + new_info["rp_era"] * ip_to_num(new_info["rp_ip"])) / ip_to_num(add_ip(old_info["rp_ip"], new_info["rp_ip"]))
        old_info["rp_whip"] = (old_info["rp_whip"] * ip_to_num(old_info["rp_ip"]) + new_info["rp_whip"] * ip_to_num(new_info["rp_ip"])) / ip_to_num(add_ip(old_info["rp_ip"], new_info["rp_ip"]))
    old_info["sp_hra"] += new_info["sp_hra"]
    old_info["sp_hitsallowed"] += new_info["sp_hitsallowed"]
    old_info["sp_k"] += new_info["sp_k"]
    old_info["sp_bb"] += new_info["sp_bb"]
    old_info["rp_hra"] += new_info["rp_hra"]
    old_info["rp_hitsallowed"] += new_info["rp_hitsallowed"]
    old_info["rp_k"] += new_info["rp_k"]
    old_info["rp_bb"] += new_info["rp_bb"]
    old_info["pa"] += new_info["pa"]
    old_info["gs"] += new_info["gs"]
    old_info["g"] += new_info["g"]
    old_info["runsscored"] += new_info["runsscored"]
    old_info["rbi"] += new_info["rbi"]
    old_info["intentionallywalked"] += new_info["intentionallywalked"]
    old_info["sacflies"] += new_info["sacflies"]
    old_info["sacbunts"] += new_info["sacbunts"]
    old_info["gidp"] += new_info["gidp"]
    old_info["stolenbases"] += new_info["stolenbases"]
    old_info["caughtstealing"] += new_info["caughtstealing"]
    old_info["ab"] += new_info["ab"]
    old_info["sp_ip"] = add_ip(old_info["sp_ip"], new_info["sp_ip"])
    old_info["sp_war"] += new_info["sp_war"]
    old_info["rp_ip"] = add_ip(old_info["rp_ip"], new_info["rp_ip"])
    old_info["rp_war"] += new_info["rp_war"]
    old_info["fieldingip"] = add_ip(old_info["fieldingip"], new_info["fieldingip"])
    old_info["bwar"] += new_info["bwar"]
    old_info["wraa"] += new_info["wraa"]
    old_info["batr"] += new_info["batr"]
    old_info["sp_bf"] += new_info["sp_bf"]
    old_info["rp_bf"] += new_info["rp_bf"]
    old_info["games"] += new_info["games"]
    old_info["gamesstarted"] += new_info["gamesstarted"]
    old_info["wsb"] += new_info["wsb"]
    old_info["ubr"] += new_info["ubr"]
    old_info["baserunningruns"] += new_info["baserunningruns"]
    old_info["bsrunchances"] += new_info["bsrunchances"]
    old_info["stealchances"] += new_info["stealchances"]
    old_info["zr"] += new_info["zr"]
    old_info["strikeouts"] += new_info["strikeouts"]
    old_info["walks"] += new_info["walks"]
    old_info["homeruns"] += new_info["homeruns"]
    old_info["hits"] += new_info["hits"]
    old_info["doubles"] += new_info["doubles"]
    old_info["triples"] += new_info["triples"]
    old_info["routinebiz"] += new_info["routinebiz"]
    old_info["routinebizfield"] += new_info["routinebizfield"]
    old_info["likelybiz"] += new_info["likelybiz"]
    old_info["likelybizfield"] += new_info["likelybizfield"]
    old_info["evenbiz"] += new_info["evenbiz"]
    old_info["evenbizfield"] += new_info["evenbizfield"]
    old_info["unlikelybiz"] += new_info["unlikelybiz"]
    old_info["unlikelybizfield"] += new_info["unlikelybizfield"]
    old_info["veryunlikelybiz"] += new_info["veryunlikelybiz"]
    old_info["veryunlikelybizfield"] += new_info["veryunlikelybizfield"]
    old_info["impossiblebiz"] += new_info["impossiblebiz"]
    old_info["totalbiz"] += new_info["totalbiz"]
    old_info["totalchances"] += new_info["totalchances"]
    old_info["assists"] += new_info["assists"]
    old_info["putouts"] += new_info["putouts"]
    old_info["stolenbaseattempts"] += new_info["stolenbaseattempts"]
    old_info["runnersthrownout"] += new_info["runnersthrownout"]
    old_info["errors"] += new_info["errors"]
    old_info["doubleplays"] += new_info["doubleplays"]
    old_info["sp_playershitbypitch"] += new_info["sp_playershitbypitch"]
    old_info["rp_playershitbypitch"] += new_info["rp_playershitbypitch"]
    old_info["timeshitbypitch"] += new_info["timeshitbypitch"]
    old_info["totalplaysfielded"] += new_info["totalplaysfielded"]
    old_info["sp_wildpitches"] += new_info["sp_wildpitches"]
    old_info["sp_pitch_stealchances"] += new_info["sp_pitch_stealchances"]
    old_info["sp_pitch_basesstolen"] += new_info["sp_pitch_basesstolen"]
    old_info["sp_pitch_stealattempts"] += new_info["sp_pitch_stealattempts"]
    old_info["sp_pitch_basesstolen_wild_pitch"] += new_info["sp_pitch_basesstolen_wild_pitch"]
    old_info["sp_earned_runs"] += new_info["sp_earned_runs"]
    old_info["sp_pitch_non_hr_hits"] += new_info["sp_pitch_non_hr_hits"]
    old_info["sp_bb_hp"] += new_info["sp_bb_hp"]
    old_info["sp_pitcherdoubleplays"] += new_info["sp_pitcherdoubleplays"]
    old_info["rp_wildpitches"] += new_info["rp_wildpitches"]
    old_info["rp_pitch_stealchances"] += new_info["rp_pitch_stealchances"]
    old_info["rp_pitch_basesstolen"] += new_info["rp_pitch_basesstolen"]
    old_info["rp_pitch_stealattempts"] += new_info["rp_pitch_stealattempts"]
    old_info["rp_pitch_basesstolen_wild_pitch"] += new_info["rp_pitch_basesstolen_wild_pitch"]
    old_info["rp_earned_runs"] += new_info["rp_earned_runs"]
    old_info["rp_pitch_non_hr_hits"] += new_info["rp_pitch_non_hr_hits"]
    old_info["rp_bb_hp"] += new_info["rp_bb_hp"]
    old_info["rp_pitcherdoubleplays"] += new_info["rp_pitcherdoubleplays"]


    if old_info["totalbiz"] > 0:
        old_info["playpct"] = old_info["totalplaysfielded"] / old_info["totalbiz"]
        old_info["routinefieldpct"] = old_info["routinebiz"] / old_info["totalbiz"]
        old_info["routinebizpct"] = old_info["routinebizfield"] / old_info["routinebiz"] if old_info["routinebiz"] > 0 else 0
        old_info["likelybizpct"] = old_info["likelybizfield"] / old_info["likelybiz"] if old_info["likelybiz"] > 0 else 0
        old_info["evenbizpct"] = old_info["evenbizfield"] / old_info["evenbiz"] if old_info["evenbiz"] > 0 else 0
        old_info["unlikelybizpct"] = old_info["unlikelybizfield"] / old_info["unlikelybiz"] if old_info["unlikelybiz"] > 0 else 0
        old_info["veryunlikelybizpct"] = old_info["veryunlikelybizfield"] / old_info["veryunlikelybiz"] if old_info["veryunlikelybiz"] > 0 else 0
    return old_info

# Meant to be able to differentiate between starter stats and reliever stats
def _read_pitcher_data(player_type, stat_type, stat):
    if player_type == stat_type:
        return stat
    return 0