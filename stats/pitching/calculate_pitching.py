from stats.pitching.regress_pitchers import regress_pitchers
from output_utils.progress.progress_bar import ProgressBar

def calculate_pitching_stats(cards, vl_data, vr_data, splits):
    sp_ratings = [
        ("stu", lambda pi: pi["sp_k"], lambda pi: pi["sp_bf"] - pi["sp_playershitbypitch"] - pi["sp_bb"]), 
        ("mov", lambda pi: pi["sp_hra"], lambda pi: pi["sp_bf"] - pi["sp_k"] - pi["sp_bb"] - pi["sp_playershitbypitch"]), 
        ("ctl", lambda pi: pi["sp_bb"], lambda pi: pi["sp_bf"] - pi["sp_playershitbypitch"])
    ]
    rp_ratings = [
        ("stu", lambda pi: pi["rp_k"], lambda pi: pi["rp_bf"] - pi["rp_playershitbypitch"] - pi["rp_bb"]), 
        ("mov", lambda pi: pi["rp_hra"], lambda pi: pi["rp_bf"] - pi["rp_k"] - pi["rp_bb"] - pi["rp_playershitbypitch"]), 
        ("ctl", lambda pi: pi["rp_bb"], lambda pi: pi["rp_bf"] - pi["rp_playershitbypitch"])
    ]
    hands = ["L", "R"]

    pitcher_regs = {
        "sp": {
            "VL": {
                "L": {},
                "R": {}
            },
            "VR": {
                "L": {},
                "R": {}
            }
        },
        "rp": {
            "VL": {
                "L": {},
                "R": {}
            },
            "VR": {
                "L": {},
                "R": {}
            }
        }
    }

    progress_bar = ProgressBar(4, "Regressing pitchers")

    for rating_key, get_val, get_true_bf in sp_ratings:
        for hand in hands:
            reg_params, reg_r2 = regress_pitchers(
                vl_data,
                rating_key,
                get_val,
                get_true_bf,
                hand,
                "VL"
            )
            pitcher_regs["sp"]["VL"][hand][rating_key] = lambda pi: reg_params[0] + reg_params[1] * pi[rating_key + "VL"]
            pitcher_regs["sp"]["VL"][hand][rating_key + "_r2"] = reg_r2
    progress_bar.increment()

    for rating_key, get_val, get_true_bf in sp_ratings:
        for hand in hands:
            reg_params, reg_r2 = regress_pitchers(
                vr_data,
                rating_key,
                get_val,
                get_true_bf,
                hand,
                "VR"
            )
            pitcher_regs["sp"]["VR"][hand][rating_key] = lambda pi: reg_params[0] + reg_params[1] * pi[rating_key + "VR"]
            pitcher_regs["sp"]["VR"][hand][rating_key + "_r2"] = reg_r2
    progress_bar.increment()

    for rating_key, get_val, get_true_bf in rp_ratings:
        for hand in hands:
            reg_params, reg_r2 = regress_pitchers(
                vl_data,
                rating_key,
                get_val,
                get_true_bf,
                hand,
                "VL"
            )
            pitcher_regs["rp"]["VL"][hand][rating_key] = lambda pi: reg_params[0] + reg_params[1] * pi[rating_key + "VL"]
            pitcher_regs["rp"]["VL"][hand][rating_key + "_r2"] = reg_r2
    progress_bar.increment()

    for rating_key, get_val, get_true_bf in rp_ratings:
        for hand in hands:
            reg_params, reg_r2 = regress_pitchers(
                vr_data,
                rating_key,
                get_val,
                get_true_bf,
                hand,
                "VR"
            )
            pitcher_regs["rp"]["VR"][hand][rating_key] = lambda pi: reg_params[0] + reg_params[1] * pi[rating_key + "VR"]
            pitcher_regs["rp"]["VR"][hand][rating_key + "_r2"] = reg_r2
    progress_bar.finish()

    print()
    print("SP VL lefty stu r2:", pitcher_regs["sp"]["VL"]["L"]["stu_r2"])
    print("SP VL lefty mov r2:", pitcher_regs["sp"]["VL"]["L"]["mov_r2"])
    print("SP VL lefty ctl r2:", pitcher_regs["sp"]["VL"]["L"]["ctl_r2"])
    print("SP VL righty stu r2:", pitcher_regs["sp"]["VL"]["R"]["stu_r2"])
    print("SP VL righty mov r2:", pitcher_regs["sp"]["VL"]["R"]["mov_r2"])
    print("SP VL righty ctl r2:", pitcher_regs["sp"]["VL"]["R"]["ctl_r2"])
    print("SP VR lefty stu r2:", pitcher_regs["sp"]["VR"]["L"]["stu_r2"])
    print("SP VR lefty mov r2:", pitcher_regs["sp"]["VR"]["L"]["mov_r2"])
    print("SP VR lefty ctl r2:", pitcher_regs["sp"]["VR"]["L"]["ctl_r2"])
    print("SP VR righty stu r2:", pitcher_regs["sp"]["VR"]["R"]["stu_r2"])
    print("SP VR righty mov r2:", pitcher_regs["sp"]["VR"]["R"]["mov_r2"])
    print("SP VR righty ctl r2:", pitcher_regs["sp"]["VR"]["R"]["ctl_r2"])
    print("RP VL lefty stu r2:", pitcher_regs["rp"]["VL"]["L"]["stu_r2"])
    print("RP VL lefty mov r2:", pitcher_regs["rp"]["VL"]["L"]["mov_r2"])
    print("RP VL lefty ctl r2:", pitcher_regs["rp"]["VL"]["L"]["ctl_r2"])
    print("RP VL righty stu r2:", pitcher_regs["rp"]["VL"]["R"]["stu_r2"])
    print("RP VL righty mov r2:", pitcher_regs["rp"]["VL"]["R"]["mov_r2"])
    print("RP VL righty ctl r2:", pitcher_regs["rp"]["VL"]["R"]["ctl_r2"])
    print("RP VR lefty stu r2:", pitcher_regs["rp"]["VR"]["L"]["stu_r2"])
    print("RP VR lefty mov r2:", pitcher_regs["rp"]["VR"]["L"]["mov_r2"])
    print("RP VR lefty ctl r2:", pitcher_regs["rp"]["VR"]["L"]["ctl_r2"])
    print("RP VR righty stu r2:", pitcher_regs["rp"]["VR"]["R"]["stu_r2"])
    print("RP VR righty mov r2:", pitcher_regs["rp"]["VR"]["R"]["mov_r2"])
    print("RP VR righty ctl r2:", pitcher_regs["rp"]["VR"]["R"]["ctl_r2"])
    print()

    progress_bar = ProgressBar(len(cards), "Writing fip data")
    for card in cards:
        for position in pitcher_regs.keys():
            for mod in pitcher_regs[position].keys():
                regs = pitcher_regs[position][mod][card["throws"]]

                total_bf = 950 if position == "sp" else 300
                hbp = 7 if position == "sp" else 3
                walks = regs["ctl"](card) * (total_bf - hbp)
                strikeouts = regs["stu"](card) * (total_bf - hbp - walks)
                homeruns = regs["mov"](card) * (total_bf - hbp - walks - strikeouts)

                # 215 is just an approximated ip.
                card[position + "_FIP_" + mod] =  ((13 * homeruns) + (3 * (walks + hbp)) - (2 * strikeouts)) / 215 + 3.079

        correct_splits = splits[card["throws"]]
        card["sp_FIP"] = card["sp_FIP_VL"] * (1 - correct_splits["starter"]) + card["sp_FIP_VR"] * correct_splits["starter"]
        card["rp_FIP"] = card["rp_FIP_VL"] * (1 - correct_splits["reliever"]) + card["rp_FIP_VR"] * correct_splits["reliever"]
        progress_bar.increment()
    progress_bar.finish()

    