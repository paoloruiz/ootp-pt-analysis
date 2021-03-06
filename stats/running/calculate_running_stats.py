from output_utils.progress.progress_bar import ProgressBar
from stats.running.regress_running import regress_steal_attempts, regress_success_rate, regress_ubr

def calculate_running_stats(ovr_data, cards):
    # No wGDP
    progress_bar = ProgressBar(len(cards) + 3, "Calculating running stats")
    progress_bar.update("Regressing UBR")
    ubr_reg, ubr_r2 = regress_ubr(ovr_data)
    progress_bar.increment("Regressing steal attempts")
    ste_att_reg, ste_att_r2 = regress_steal_attempts(ovr_data)
    progress_bar.increment("Regressing success rate")
    ste_suc_reg, ste_suc_r2 = regress_success_rate(ovr_data)
    progress_bar.increment("Calculating running stats into cards")

    for card in cards:
        steal_attempts = ste_att_reg[0] + ste_att_reg[1] * card["spe"]
        success_rate = min(max(ste_suc_reg[0] + ste_suc_reg[1] * card["ste"], 1.0), 0.0)
        ubr = (ubr_reg[0] + ubr_reg[1] * card["run"]) * card["bsrunchances_ft"]
        card["steal_attempts"] = steal_attempts * success_rate
        card["caught_stealing"] = steal_attempts * (1 - success_rate)
        card["ubr"] = ubr
        progress_bar.increment()

    progress_bar.finish()

    print()
    print("Steal attempts r2:", ste_att_r2)
    print("Steal success rate r2:", ste_suc_r2)
    print("UBR r2:", ubr_r2)
    print()