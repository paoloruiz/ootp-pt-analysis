def get_splits(ovr_data, vl_data_ylt, vr_data_ylt, vl_data, vr_data):
    catcher_full_time, catcher_vr, catcher_vl = _get_potential_catchers(ovr_data, vl_data_ylt, vr_data_ylt)
    fielder_full_time, fielder_vr, fielder_vl = _get_potential_fielders(ovr_data, vl_data_ylt, vr_data_ylt)

    return {
        "FT": {
            "GS": {
                "fielder": sum(map(lambda gs_stats: gs_stats["gs"], fielder_full_time)) / len(fielder_full_time),
                "catcher": sum(map(lambda gs_stats: gs_stats["gs"], catcher_full_time)) / len(catcher_full_time)
            },
            "vR%": {
                "fielder": sum(map(lambda gs_stats: gs_stats["vr_pa"], fielder_full_time)) / sum(map(lambda gs_stats: gs_stats["vr_pa"] + gs_stats["vl_pa"], fielder_full_time)),
                "catcher": sum(map(lambda gs_stats: gs_stats["vr_pa"], catcher_full_time)) / sum(map(lambda gs_stats: gs_stats["vr_pa"] + gs_stats["vl_pa"], catcher_full_time))
            }
        },
        "vR": {
            "GS": {
                "fielder": sum(map(lambda gs_stats: gs_stats["gs"], fielder_vr)) / len(fielder_vr),
                "catcher": sum(map(lambda gs_stats: gs_stats["gs"], catcher_vr)) / len(catcher_vr) if len(catcher_vr) > 0 else 88.68275
            },
            "vR%": {
                "fielder": sum(map(lambda gs_stats: gs_stats["vr_pa"], fielder_vr)) / sum(map(lambda gs_stats: gs_stats["vr_pa"] + gs_stats["vl_pa"], fielder_vr)),
                "catcher": sum(map(lambda gs_stats: gs_stats["vr_pa"], catcher_vr)) / sum(map(lambda gs_stats: gs_stats["vr_pa"] + gs_stats["vl_pa"], catcher_vr)) if len(catcher_vr) > 0 else 0.70849
            }
        },
        "vL": {
            "GS": {
                "fielder": sum(map(lambda gs_stats: gs_stats["gs"], fielder_vl)) / len(fielder_vl),
                "catcher": sum(map(lambda gs_stats: gs_stats["gs"], catcher_vl)) / len(catcher_vl) if len(catcher_vl) > 0 else 73.61379
            },
            "vR%": {
                "fielder": sum(map(lambda gs_stats: gs_stats["vr_pa"], fielder_vl)) / sum(map(lambda gs_stats: gs_stats["vr_pa"] + gs_stats["vl_pa"], fielder_vl)),
                "catcher": sum(map(lambda gs_stats: gs_stats["vr_pa"], catcher_vl)) / sum(map(lambda gs_stats: gs_stats["vr_pa"] + gs_stats["vl_pa"], catcher_vl)) if len(catcher_vl) > 0 else 0.359298
            }
        },
        **_get_pitcher_splits(vl_data, vr_data)
    }

def _get_gs(player):
    return player["gs"]

def _get_potential_catchers(ovr_data, vl_data, vr_data):
    full_time_candidates = []
    vr_candidates = []
    vl_candidates = []
    for year_league_team in ovr_data.keys():
        roster = ovr_data[year_league_team]
        pot_catchers = []
        for cid in roster.keys():
            if not cid in vl_data[year_league_team]:
                continue
            if roster[cid]["cera"] > 2.0 and roster[cid]["gs"] > 30:
                pot_catchers.append(roster[cid])
        pot_catchers.sort(key=_get_gs, reverse=True)
        if len(pot_catchers) != 2:
            continue
        if pot_catchers[0]["gs"] + pot_catchers[1]["gs"] < 150:
            continue
        gs_stats_c_one = _get_gs_stats(pot_catchers[0], year_league_team, ovr_data, vl_data, vr_data)
        gs_stats_c_two = _get_gs_stats(pot_catchers[1], year_league_team, ovr_data, vl_data, vr_data)
        if pot_catchers[0]["gs"] > 90 and (gs_stats_c_one["vl_pa"] > gs_stats_c_two["vl_pa"]) and (gs_stats_c_one["vr_pa"] > gs_stats_c_two["vr_pa"]):
            full_time_candidates.append(_get_gs_stats(pot_catchers[0], year_league_team, ovr_data, vl_data, vr_data))
        else:
            if vl_data[year_league_team][pot_catchers[0]["CID"]]["gs"] > vl_data[year_league_team][pot_catchers[1]["CID"]]["gs"]:
                vl_candidates.append(_get_gs_stats(pot_catchers[0], year_league_team, ovr_data, vl_data, vr_data))
                vr_candidates.append(_get_gs_stats(pot_catchers[1], year_league_team, ovr_data, vl_data, vr_data))
            else:
                vl_candidates.append(_get_gs_stats(pot_catchers[1], year_league_team, ovr_data, vl_data, vr_data))
                vr_candidates.append(_get_gs_stats(pot_catchers[0], year_league_team, ovr_data, vl_data, vr_data))
    return (full_time_candidates, vr_candidates, vl_candidates)

def _get_potential_fielders(ovr_data, vl_data, vr_data):
    full_time_candidates = []
    vr_candidates = []
    vl_candidates = []
    for year_league_team in ovr_data:
        roster = ovr_data[year_league_team]
        pot_fielders = []
        for cid in roster:
            if roster[cid]["cera"] < 1.0 and roster[cid]["gs"] > 45:
                pot_fielders.append(roster[cid])
        for fielder in pot_fielders:
            if not fielder["CID"] in vl_data[year_league_team]:
                continue
            tot_gs = fielder["gs"]
            vl_gs = vl_data[year_league_team][fielder["CID"]]["gs"]

            if tot_gs > 135:
                full_time_candidates.append(_get_gs_stats(fielder, year_league_team, ovr_data, vl_data, vr_data))
            elif tot_gs > 125:
                if vl_gs / tot_gs > 0.30 or tot_gs > 140:
                    full_time_candidates.append(_get_gs_stats(fielder, year_league_team, ovr_data, vl_data, vr_data))
            if tot_gs > 80 and tot_gs < 140:
                if vl_gs / tot_gs <= 0.30:
                    vr_candidates.append(_get_gs_stats(fielder, year_league_team, ovr_data, vl_data, vr_data))
            if tot_gs > 40 and tot_gs < 82:
                if vl_gs / tot_gs > 0.5:
                    vl_candidates.append(_get_gs_stats(fielder, year_league_team, ovr_data, vl_data, vr_data))
    return (full_time_candidates, vr_candidates, vl_candidates)

def _get_gs_stats(player, year_league_team, ovr_data, vl_data, vr_data):
    return {
        "gs": ovr_data[year_league_team][player["CID"]]["gs"],
        "vl_pa": vl_data[year_league_team][player["CID"]]["pa"],
        "vr_pa": vr_data[year_league_team][player["CID"]]["pa"]
    }

def _get_pitcher_splits(vl_data, vr_data):
    slhp_v_lhb = 0
    slhp_v_rhb = 0
    srhp_v_lhb = 0
    srhp_v_rhb = 0
    rlhp_v_lhb = 0
    rlhp_v_rhb = 0
    rrhp_v_lhb = 0
    rrhp_v_rhb = 0

    for card in vl_data.values():
        if card["throws"] == "L":
            slhp_v_lhb += card["sp_bf"]
            rlhp_v_lhb += card["rp_bf"]
        else:
            srhp_v_lhb += card["sp_bf"]
            rrhp_v_lhb += card["rp_bf"]
    
    for card in vr_data.values():
        if card["throws"] == "L":
            slhp_v_rhb += card["sp_bf"]
            rlhp_v_rhb += card["rp_bf"]
        else:
            srhp_v_rhb += card["sp_bf"]
            rrhp_v_rhb += card["rp_bf"]

    return {
        "L": {
            "starter": slhp_v_rhb / (slhp_v_lhb + slhp_v_rhb),
            "reliever": rlhp_v_rhb / (rlhp_v_lhb + rlhp_v_rhb)
        },
        "R": {
            "starter": srhp_v_rhb / (srhp_v_lhb + srhp_v_rhb),
            "reliever": rrhp_v_rhb / (rrhp_v_lhb + rrhp_v_rhb)
        }
    }
