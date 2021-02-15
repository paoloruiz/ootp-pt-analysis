from card_parsing.read_cards import parse_cards
from output_utils.generate_worksheet import generate_worksheet
from output_utils.worksheet_headers import batter_headers, pitcher_headers, data_headers, batter_freeze_col, pitcher_freeze_col, data_freeze_col, data_hidden_columns, batter_hidden_columns, pitcher_hidden_columns
from stats.babip.calculate_babip import calculate_babips
from stats.woba.calculate_woba import get_woba_factors
from data_parsing.read_db import read_files_to_db

import xlsxwriter

configuration = {
    "min_level": "I",
    "min_year": 2020,
    # TODO half-implemented tourney mode - will fill out later
    "tourney_mode": False
}

cards = parse_cards()

# Perform analysis here.
# Calculate in BABIP
calculate_babips(cards)

# Read data from league files
ovr_data, vl_data, vr_data = read_files_to_db(configuration["min_level"], configuration["min_year"], cards)

# Get OOTP wOBA factors
ovr_woba_factors, vl_woba_factors, vr_woba_factors = get_woba_factors(ovr_data, vl_data, vr_data)

pitcher_cards = []
batter_cards = []

for card in cards:
    # All pitchers and batters who have stuff ratings higher than 30
    if card["position"] == "SP" or card["position"] == "RP" or card["position"] == "CL" or card["stu"] > 30:
        pitcher_cards.append(card)
    # All batters and pitchers who have overall contact higher than 40
    if ((card["position"] != "SP" and card["position"] != "RP" and card["position"] != "CL") or card["con"] > 40) and "-rp" not in str(card["t_CID"]) and "-sp" not in str(card["t_CID"]):
        batter_cards.append(card)

# Create sheet
workbook = xlsxwriter.Workbook('output/PTSheet.xlsx')
batter_sheet = workbook.add_worksheet("List-BAT")
pitcher_sheet = workbook.add_worksheet("List-PIT")
full_sheet = workbook.add_worksheet("Cards")

# Write different stats to sheet
generate_worksheet(batter_cards, batter_sheet, batter_headers, batter_freeze_col, batter_hidden_columns)
generate_worksheet(pitcher_cards, pitcher_sheet, pitcher_headers, pitcher_freeze_col, pitcher_hidden_columns)
generate_worksheet(cards, full_sheet, data_headers, data_freeze_col, data_hidden_columns)

workbook.close()