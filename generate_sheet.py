from card_parsing.read_cards import parse_cards
from stats.babip.calculate_babip import calculate_babips
from stats.woba.calculate_woba import get_woba_factors
from stats.defense.calculate_defense import calculate_defense
from stats.league_stats.calculate_league_stats import calculate_league_stats
from data_parsing.read_db import read_files_to_db
from output_utils.sheets.generate_analysis_workbook import generate_analysis_workbook
from output_utils.sheets.generate_stats_workbook import generate_stats_workbook

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

# Calculate in defensive ratings
calculate_defense(cards)

# Read data from league files
ovr_data, vl_data, vr_data = read_files_to_db(configuration["min_level"], configuration["min_year"], cards)

# Calculate league stats
calculate_league_stats(ovr_data, vl_data, vr_data)

# Get OOTP wOBA factors
ovr_woba_factors, vl_woba_factors, vr_woba_factors = get_woba_factors(ovr_data, vl_data, vr_data)

# Analysis Sheet
generate_analysis_workbook(cards)

# Stats Sheet
generate_stats_workbook(ovr_data, vl_data, vr_data)
# End Stats Sheet