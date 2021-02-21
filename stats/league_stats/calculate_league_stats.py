from util.number_utils import ip_to_num
from output_utils.progress.progress_bar import ProgressBar

def calculate_league_stats(ovr_data, vl_data, vr_data):
    tot_batr = 0.0
    tot_bsr = 0.0
    tot_zr = 0.0
    tot_pas = 0
    for player_data in ovr_data.values():
        tot_batr += player_data["batr"]
        tot_bsr += player_data["baserunningruns"]
        tot_zr += player_data["zr"]
        tot_pas += player_data["pa"]
    league_adj = -1 * (tot_batr + tot_bsr + tot_zr) / tot_pas
    replacement_player_adj = 228000 / 185553

    batter_stats = {
        "avg": lambda pd: pd["hits"] / pd["ab"] if pd["ab"] > 0 else 0,
        "obp": lambda pd: (pd["hits"] + pd["walks"] + pd["timeshitbypitch"]) / pd["pa"] if pd["pa"] > 0 else 0,
        "ops": lambda pd: (pd["hits"] + pd["doubles"] + pd["triples"] * 2 + pd["homeruns"] * 3) / pd["ab"] + (pd["hits"] + pd["walks"] + pd["timeshitbypitch"]) / pd["pa"] if pd["ab"] > 0 else 0,
        "bsr_600_pa": lambda pd: ovr_data[str(pd["t_CID"])]["baserunningruns"] * 600 / ovr_data[str(pd["t_CID"])]["pa"] if pd["pa"] > 0 else 0,
        "zr_600_pa": lambda pd: pd["zr"] * 600 / pd["pa"] if pd["pa"] > 0 else 0,
        "batr_600_pa": lambda pd: pd["batr"] * 600 / pd["pa"] if pd["pa"] > 0 else 0,
        # last number is replacement adjustment, so it's not based on average
        "war_600_pa": lambda pd: (pd["batr"] + pd["zr"] + pd["baserunningruns"] + league_adj + replacement_player_adj) * 600 / (pd["pa"] * 10) if pd["pa"] > 0 else 0
    }

    pitcher_stats = {
        "sp_k_per_9": lambda pd: pd["sp_k"] * 9 / ip_to_num(pd["sp_ip"]) if pd["sp_ip"] > 0 else 0,
        "sp_bb_with_hbp_per_9": lambda pd: (pd["sp_bb"] + pd["sp_playershitbypitch"]) * 9 / ip_to_num(pd["sp_ip"]) if pd["sp_ip"] > 0 else 0,
        "sp_hr_per_9": lambda pd: pd["sp_hra"] * 9 / ip_to_num(pd["sp_ip"]) if pd["sp_ip"] > 0 else 0,
        "rp_k_per_9": lambda pd: pd["rp_k"] * 9 / ip_to_num(pd["rp_ip"]) if pd["rp_ip"] > 0 else 0,
        "rp_bb_with_hbp_per_9": lambda pd: (pd["rp_bb"] + pd["rp_playershitbypitch"]) * 9 / ip_to_num(pd["rp_ip"]) if pd["rp_ip"] > 0 else 0,
        "rp_hr_per_9": lambda pd: pd["rp_hra"] * 9 / ip_to_num(pd["rp_ip"]) if pd["rp_ip"] > 0 else 0,
        "ip_per_gamesstarted": lambda pd: pd["sp_ip"] / pd["gamesstarted"] if pd["gamesstarted"] > 0 and pd["gamesstarted"] == pd["games"] else 0,
        "ip_per_gamesrelieved": lambda pd: pd["rp_ip"] / pd["games"] if pd["games"] > 0 and pd["gamesstarted"] == 0 else 0,
        "sp_war_per_220_ip": lambda pd: pd["sp_war"] * 220 / ip_to_num(pd["sp_ip"]) if pd["sp_ip"] > 0 else -50,
        "rp_war_per_100_ip": lambda pd: pd["rp_war"] * 100 / ip_to_num(pd["rp_ip"]) if pd["rp_ip"] > 0 else 0,
    }

    _calculate_stats_per_data(ovr_data, batter_stats, pitcher_stats, "ovr")
    _calculate_stats_per_data(vl_data, batter_stats, pitcher_stats, "vL")
    _calculate_stats_per_data(vr_data, batter_stats, pitcher_stats, "vR")
    print()

def _calculate_stats_per_data(data, batter_lambdas, pitcher_lambdas, stats_type):
    progress_bar = ProgressBar(len(data.keys()), "Generating " + stats_type + " stats sheet")
    for card in data.values():
        for batter_name in batter_lambdas.keys():
            card[batter_name] = batter_lambdas[batter_name](card)
        for pitcher_name in pitcher_lambdas.keys():
            card[pitcher_name] = pitcher_lambdas[pitcher_name](card)

        progress_bar.increment()
    progress_bar.finish()

    