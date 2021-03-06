from output_utils.progress.progress_bar import ProgressBar

def get_hbp_stats(ovr_data):
    pitcher_db = {}
    progress_bar = ProgressBar(len(ovr_data.keys()), "Reading pitcher HBP stats")
    for card in ovr_data.values():
        if card["sp_bf"] > 20 or card["rp_bf"] > 20:
            pitcher_db[card["t_CID"]] = (card["sp_playershitbypitch"] + card["rp_playershitbypitch"]) / (card["sp_bf"] +  card["rp_bf"])

        progress_bar.increment()

    progress_bar.finish()
    return pitcher_db