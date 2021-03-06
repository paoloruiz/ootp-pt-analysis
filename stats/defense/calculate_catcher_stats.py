from stats.defense.regress_catcher_defense import regress_cera, regress_rto
from output_utils.progress.progress_bar import ProgressBar

def calculate_catcher_stats(ovr_data, cards):
    progress_bar = ProgressBar(len(cards) + 2, "Updating cards with catcher defensive stats")
    progress_bar.update("Regressing cera")
    cera_params, cera_r2 = regress_cera(ovr_data)
    progress_bar.increment("Regressing rto")
    att_per_inning_params, att_per_arm_r2, rto_per_att_params, rto_per_att_r2, avg_carm, avg_cabi = regress_rto(ovr_data)
    progress_bar.increment("Updating cards with catcher defense stats")
    for card in cards:
        card["cera_effect_runs_saved"] = ((cera_params[1] * card["cabi"]) - cera_params[1] * avg_cabi) * -162
        expected_attempts = (att_per_inning_params[0] + att_per_inning_params[1] * card["carm"]) * 9 * 162
        expected_rto = rto_per_att_params[0] + rto_per_att_params[1] * card["carm"]
        avg_expected_attempts = (att_per_inning_params[0] + att_per_inning_params[1] * avg_carm) * 9 * 162
        avg_expected_rto = rto_per_att_params[0] + rto_per_att_params[1] * avg_carm
        card["expected_rto_above_avg"] = expected_attempts * expected_rto - avg_expected_attempts * avg_expected_rto
        card["expected_steals_given_up_above_avg"] = expected_attempts * (1 - expected_rto) - avg_expected_attempts * (1 - avg_expected_rto)
        progress_bar.increment()
    progress_bar.finish()

    print()
    print("CERA r2:", cera_r2)
    print("Attempts per year r2:", att_per_arm_r2)
    print("Runners thrown out per attempt r2:", rto_per_att_r2)
    print()