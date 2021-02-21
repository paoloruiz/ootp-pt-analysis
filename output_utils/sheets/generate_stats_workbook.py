from output_utils.headers.stats_sheet_headers import (
    batter_stats_headers, batter_stats_hidden_columns, batter_stats_freeze_col, 
    sp_stats_headers, sp_stats_hidden_columns, sp_stats_freeze_col, 
    rp_stats_headers, rp_stats_hidden_columns, rp_stats_freeze_col
)
from output_utils.sheets.generate_worksheet import generate_worksheet
from output_utils.progress.progress_bar import ProgressBar
import xlsxwriter

def generate_stats_workbook(ovr_data, vl_data, vr_data):
    batter_ovr_stats_cards = []
    sp_ovr_stats_cards = []
    rp_ovr_stats_cards = []

    progress_bar = ProgressBar(len(ovr_data.keys()) + len(vl_data.keys()) + len(vr_data.keys()), "Sorting cards for sheet statistics")

    for card in ovr_data.values():
        if card["pa"] > 10:
            batter_ovr_stats_cards.append(card)
        if card["sp_ip"] > 5:
            sp_ovr_stats_cards.append(card)
        if card["rp_ip"] > 5:
            rp_ovr_stats_cards.append(card)
        progress_bar.increment()

    batter_vl_stats_cards = []
    sp_vl_stats_cards = []
    rp_vl_stats_cards = []

    for card in vl_data.values():
        if card["pa"] > 10:
            batter_vl_stats_cards.append(card)
        if card["sp_ip"] > 5:
            sp_vl_stats_cards.append(card)
        if card["rp_ip"] > 5:
            rp_vl_stats_cards.append(card)
        progress_bar.increment()

    batter_vr_stats_cards = []
    sp_vr_stats_cards = []
    rp_vr_stats_cards = []

    for card in vr_data.values():
        if card["pa"] > 10:
            batter_vr_stats_cards.append(card)
        if card["sp_ip"] > 5:
            sp_vr_stats_cards.append(card)
        if card["rp_ip"] > 5:
            rp_vr_stats_cards.append(card)
        progress_bar.increment()
    progress_bar.finish()

    sheet_pbar = ProgressBar(1, "Creating stats sheet")
    workbook = xlsxwriter.Workbook('output/PTStatsSheet.xlsx')
    batter_ovr_stats_sheet = workbook.add_worksheet("BAT-Ovr")
    batter_vl_stats_sheet = workbook.add_worksheet("BAT-vL")
    batter_vr_stats_sheet = workbook.add_worksheet("BAT-vR")
    sp_ovr_stats_sheet = workbook.add_worksheet("SP-Ovr")
    sp_vl_stats_sheet = workbook.add_worksheet("SP-vL")
    sp_vr_stats_sheet = workbook.add_worksheet("SP-vR")
    rp_ovr_stats_sheet = workbook.add_worksheet("RP-Ovr")
    rp_vl_stats_sheet = workbook.add_worksheet("RP-vL")
    rp_vr_stats_sheet = workbook.add_worksheet("RP-vR")
    sheet_pbar.finish()

    # Sort cards for sheet
    sort_pbar = ProgressBar(9, "Sorted all cards")
    sort_pbar.update("Sorting ovr batter cards")
    batter_ovr_stats_cards.sort(key=lambda pd: pd["war_600_pa"], reverse=True)
    sort_pbar.increment("Sorting vL batter cards")
    batter_vl_stats_cards.sort(key=lambda pd: pd["war_600_pa"], reverse=True)
    sort_pbar.increment("Sorting vR batter cards")
    batter_vr_stats_cards.sort(key=lambda pd: pd["war_600_pa"], reverse=True)
    sort_pbar.increment("Sorting ovr SP cards")
    sp_ovr_stats_cards.sort(key=lambda pd: pd["sp_war_per_220_ip"], reverse=True)
    sort_pbar.increment("Sorting vL SP cards")
    sp_vl_stats_cards.sort(key=lambda pd: pd["sp_war_per_220_ip"], reverse=True)
    sort_pbar.increment("Sorting vR SP cards")
    sp_vr_stats_cards.sort(key=lambda pd: pd["sp_war_per_220_ip"], reverse=True)
    sort_pbar.increment("Sorting ovr RP cards")
    rp_ovr_stats_cards.sort(key=lambda pd: pd["rp_war_per_100_ip"], reverse=True)
    sort_pbar.increment("Sorting vL RP cards")
    rp_vl_stats_cards.sort(key=lambda pd: pd["rp_war_per_100_ip"], reverse=True)
    sort_pbar.increment("Sorting vR RP cards")
    rp_vr_stats_cards.sort(key=lambda pd: pd["rp_war_per_100_ip"], reverse=True)
    sort_pbar.finish()

    generate_worksheet(batter_ovr_stats_cards, batter_ovr_stats_sheet, batter_stats_headers, batter_stats_freeze_col, batter_stats_hidden_columns, "batter ovr stats")
    generate_worksheet(batter_vl_stats_cards, batter_vl_stats_sheet, batter_stats_headers, batter_stats_freeze_col, batter_stats_hidden_columns, "batter vL stats")
    generate_worksheet(batter_vr_stats_cards, batter_vr_stats_sheet, batter_stats_headers, batter_stats_freeze_col, batter_stats_hidden_columns, "batter vR stats")
    generate_worksheet(sp_ovr_stats_cards, sp_ovr_stats_sheet, sp_stats_headers, sp_stats_freeze_col, sp_stats_hidden_columns, "sp ovr stats")
    generate_worksheet(sp_vl_stats_cards, sp_vl_stats_sheet, sp_stats_headers, sp_stats_freeze_col, sp_stats_hidden_columns, "sp vL stats")
    generate_worksheet(sp_vr_stats_cards, sp_vr_stats_sheet, sp_stats_headers, sp_stats_freeze_col, sp_stats_hidden_columns, "sp vR stats")
    generate_worksheet(rp_ovr_stats_cards, rp_ovr_stats_sheet, rp_stats_headers, rp_stats_freeze_col, rp_stats_hidden_columns, "rp ovr stats")
    generate_worksheet(rp_vl_stats_cards, rp_vl_stats_sheet, rp_stats_headers, rp_stats_freeze_col, rp_stats_hidden_columns, "rp vL stats")
    generate_worksheet(rp_vr_stats_cards, rp_vr_stats_sheet, rp_stats_headers, rp_stats_freeze_col, rp_stats_hidden_columns, "rp vR stats")

    close_pbar = ProgressBar(1, "Closing stats sheet file")
    workbook.close()
    close_pbar.finish()
    print()