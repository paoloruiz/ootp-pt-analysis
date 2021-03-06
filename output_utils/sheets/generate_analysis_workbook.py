from output_utils.headers.analysis_sheet_headers import batter_headers, pitcher_headers, data_headers, batter_freeze_col, pitcher_freeze_col, data_freeze_col, data_hidden_columns, batter_hidden_columns, pitcher_hidden_columns
from output_utils.sheets.generate_worksheet import generate_worksheet
from output_utils.progress.progress_bar import ProgressBar
import xlsxwriter

def generate_analysis_workbook(cards):
    pitcher_cards = []
    batter_cards = []

    progress_bar = ProgressBar(len(cards), "Sorting cards for analysis")
    for card in cards:
        # All pitchers and batters who have stuff ratings higher than 30
        if card["position"] == "SP" or card["position"] == "RP" or card["position"] == "CL" or card["stu"] > 30:
            pitcher_cards.append(card)
        # All batters and pitchers who have overall contact higher than 40
        if ((card["position"] != "SP" and card["position"] != "RP" and card["position"] != "CL") or card["con"] > 40) and "-rp" not in str(card["t_CID"]) and "-sp" not in str(card["t_CID"]):
            batter_cards.append(card)
        progress_bar.increment()
    progress_bar.finish()

    # Create sheet
    sheet_pbar = ProgressBar(1, "Creating stats sheet")
    workbook = xlsxwriter.Workbook('output/PTSheet.xlsx')
    batter_sheet = workbook.add_worksheet("List-BAT")
    pitcher_sheet = workbook.add_worksheet("List-PIT")
    full_sheet = workbook.add_worksheet("Cards")
    sheet_pbar.finish()

    batter_cards.sort(key=lambda pd: pd["wOBA_ft_starter"], reverse=True)
    pitcher_cards.sort(key=lambda pd: pd["sp_FIP"])

    # Write different stats to sheet
    generate_worksheet(batter_cards, batter_sheet, batter_headers, batter_freeze_col, batter_hidden_columns, "batter analysis")
    generate_worksheet(pitcher_cards, pitcher_sheet, pitcher_headers, pitcher_freeze_col, pitcher_hidden_columns, "pitcher analysis")
    generate_worksheet(cards, full_sheet, data_headers, data_freeze_col, data_hidden_columns, "cards analysis")

    close_pbar = ProgressBar(1, "Closing analysis sheet file")
    workbook.close()
    close_pbar.finish()
    print()