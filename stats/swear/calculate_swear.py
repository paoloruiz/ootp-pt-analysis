from output_utils.progress.progress_bar import ProgressBar

# scipper's Wins expected Above Replacement
def calculate_swear(cards, woba_ovr_factors, woba_vl_factors, woba_vr_factors, splits):

    progress_bar = ProgressBar(len(cards), "Adding in sWeAR")
    positions = ["C", "1B", "2B", "3B", "SS", "LF", "CF", "RF", "DH"]
    for card in cards:
        # wOBA scale already incorporated into this
        vl_wraa = (card["wOBA_vL"] - woba_vl_factors["lg_woba"]) * 720
        vr_wraa = (card["wOBA_vR"] - woba_vr_factors["lg_woba"]) * 720
        wSB_vL = card["steal_successes"] * woba_ovr_factors["runSB"] + card["caught_stealing"] * woba_ovr_factors["runCS"] - woba_ovr_factors["lgwSB"] * (card["singles_vL"] + card["BB_vL"] + card["HBP_vL"])
        wSB_vR = card["steal_successes"] * woba_ovr_factors["runSB"] + card["caught_stealing"] * woba_ovr_factors["runCS"] - woba_ovr_factors["lgwSB"] * (card["singles_vR"] + card["BB_vR"] + card["HBP_vR"])
        ubr = card["ubr"]

        for position in positions:
            if position == "DH":
                # Adjust to the fact that DH hit a bit worse.
                defensive_runs_saved = -7.5
                card["sWeAR_ft_" + position] = ((vl_wraa * (1 - splits["FT"]["vR%"]["fielder"]) + vr_wraa * splits["FT"]["vR%"]["fielder"] + wSB_vL * (1 - splits["FT"]["vR%"]["fielder"]) 
                    + wSB_vR * splits["FT"]["vR%"]["fielder"] + ubr + defensive_runs_saved) / woba_ovr_factors["runs_per_win"]) / 162 * splits["FT"]["GS"]["fielder"]
                card["sWeAR_vL_starter_" + position] = ((vl_wraa * (1 - splits["vL"]["vR%"]["fielder"]) + vr_wraa * splits["vL"]["vR%"]["fielder"] + wSB_vL * (1 - splits["vL"]["vR%"]["fielder"]) 
                    + wSB_vR * splits["vL"]["vR%"]["fielder"] + ubr + defensive_runs_saved) / woba_ovr_factors["runs_per_win"]) / 162 * splits["vL"]["GS"]["fielder"]
                card["sWeAR_vR_starter_" + position] = ((vl_wraa * (1 - splits["vR"]["vR%"]["fielder"]) + vr_wraa * splits["vR"]["vR%"]["fielder"] + wSB_vL * (1 - splits["vR"]["vR%"]["fielder"]) 
                    + wSB_vR * splits["vR"]["vR%"]["fielder"] + ubr + defensive_runs_saved) / woba_ovr_factors["runs_per_win"]) / 162 * splits["vR"]["GS"]["fielder"]
                continue

            # Switch these off to test different ways of using defensive WAR stats for sWeAR
            defensive_runs_saved = _get_zr_defensive_stat(card, position, woba_ovr_factors) * _get_positional_multiplier(position)
            # defensive_runs_saved = _get_outs_above_average_defensive_stat(card, position, woba_ovr_factors)

            extra_catcher_effects = 0
            pos_mod = "fielder"
            if position == "C":
                extra_catcher_effects = card["cera_effect_runs_saved"] + card["expected_rto_above_avg"] * woba_ovr_factors["outs_per_run"] * -1 - card["expected_steals_given_up_above_avg"] * woba_ovr_factors["runSB"]
                pos_mod = "catcher"
            
            card["sWeAR_ft_" + position] = ((vl_wraa * (1 - splits["FT"]["vR%"][pos_mod]) + vr_wraa * splits["FT"]["vR%"][pos_mod] + wSB_vL * (1 - splits["FT"]["vR%"][pos_mod]) 
                + wSB_vR * splits["FT"]["vR%"][pos_mod] + ubr + defensive_runs_saved + extra_catcher_effects) / woba_ovr_factors["runs_per_win"]) / 162 * splits["FT"]["GS"][pos_mod]
            card["sWeAR_vL_starter_" + position] = ((vl_wraa * (1 - splits["vL"]["vR%"][pos_mod]) + vr_wraa * splits["vL"]["vR%"][pos_mod] + wSB_vL * (1 - splits["vL"]["vR%"][pos_mod]) 
                + wSB_vR * splits["vL"]["vR%"][pos_mod] + ubr + defensive_runs_saved + extra_catcher_effects) / woba_ovr_factors["runs_per_win"]) / 162 * splits["vL"]["GS"][pos_mod]
            card["sWeAR_vR_starter_" + position] = ((vl_wraa * (1 - splits["vR"]["vR%"][pos_mod]) + vr_wraa * splits["vR"]["vR%"][pos_mod] + wSB_vL * (1 - splits["vR"]["vR%"][pos_mod]) 
                + wSB_vR * splits["vR"]["vR%"][pos_mod] + ubr + defensive_runs_saved + extra_catcher_effects) / woba_ovr_factors["runs_per_win"]) / 162 * splits["vR"]["GS"][pos_mod]
        progress_bar.increment()
    progress_bar.finish()
    
def _get_zr_defensive_stat(card, position, woba_ovr_factors):
    return card[position + "_expected_zr"]

def _get_outs_above_average_defensive_stat(card, position, woba_ovr_factors):
    # The -1 is because it's a positive if a defender gets someone out
    return card[position + "_expected_outs_above_avg"] * woba_ovr_factors["outs_per_run"] * -1

# Get a positional adjustment for adjusting position, these probably need some manually adjusted
positional_adjustment = {
    "C": 1.0,
    "1B": 0.3,
    "2B": 0.5,
    "3B": 0.4,
    "SS": 1.5,
    "LF": 0.4,
    "CF": 1.0,
    "RF": 0.4
}
def _get_positional_multiplier(position):
    return positional_adjustment[position]