from output_utils.progress.progress_bar import ProgressBar

def get_hbp_stats(ovr_data):
    batter_db = {}
    progress_bar = ProgressBar(len(ovr_data.keys()), "Reading HBP stats")
    for card in ovr_data.values():
        if card["pa"] > 50:
            batter_db[card["t_CID"]] = card["timeshitbypitch"] / card["pa"]

        progress_bar.increment()

    progress_bar.finish()
    return batter_db