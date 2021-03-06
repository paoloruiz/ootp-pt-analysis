from card_parsing.read_cards import parse_cards
from stats.babip.calculate_babip import calculate_babips
from stats.woba.calculate_woba import get_woba_factors
from stats.defense.calculate_defense import calculate_defense
from stats.defense.calculate_defensive_stats import calculate_defensive_stats
from stats.defense.calculate_catcher_stats import calculate_catcher_stats
from stats.league_stats.calculate_league_stats import calculate_league_stats
from stats.hitting.calculate_hitting_stats import calculate_hitting_stats
from stats.hitting.calculate_hbp_stats import get_hbp_stats
from stats.running.calculate_running_stats import calculate_running_stats
from stats.splits.calculate_splits import get_splits
from stats.swear.calculate_swear import calculate_swear
from stats.pitching.calculate_pitching import calculate_pitching_stats
from data_parsing.read_db import read_files_to_db
from data_parsing.read_tourney_data import get_stats_from_db_tourney
from output_utils.sheets.generate_analysis_workbook import generate_analysis_workbook
from output_utils.sheets.generate_stats_workbook import generate_stats_workbook
import time
import copy

start = time.process_time()

configuration = {
    "min_level": "I",
    "min_year": 2020,
    # TODO un-implemented tourney mode - you can set this to analyze tournaments specifically instead of full PT mode. You'll need to implement this for yourself. (alternatively just implement the stats mode)
    "tourney_mode": False
}

cards = parse_cards()

# Perform analysis here.
# Calculate in BABIP
calculate_babips(cards)

# Calculate in defensive ratings
calculate_defense(cards)

tourney_cards = copy.deepcopy(cards)

perfect_level_tourney_db = get_stats_from_db_tourney("P", tourney_cards)

# Read data from league files
ovr_data, vl_data, vr_data, ovr_data_ylt, vl_data_ylt, vr_data_ylt = read_files_to_db(configuration["min_level"], configuration["min_year"], cards)

# Calculate splits on full-time/part-time fielders and catchers
splits = get_splits(ovr_data_ylt, vl_data_ylt, vr_data_ylt, vl_data, vr_data)

# Calculate HBP rate
batter_hbp_rate = get_hbp_stats(ovr_data)

# Calculate league stats
calculate_league_stats(ovr_data, vl_data, vr_data, splits)

# Get OOTP wOBA factors
ovr_woba_factors, vl_woba_factors, vr_woba_factors = get_woba_factors(ovr_data, vl_data, vr_data)

# Calculate hitting stats
calculate_hitting_stats(cards, vl_data, vr_data, ovr_woba_factors, vl_woba_factors, vr_woba_factors, splits, batter_hbp_rate)

# Fielding stats
calculate_defensive_stats(perfect_level_tourney_db, cards)

# Catcher-specific fielding stats
calculate_catcher_stats(ovr_data, cards)

# Running stats
calculate_running_stats(ovr_data, cards)

# Calculate sWeAR
calculate_swear(cards, ovr_woba_factors, vl_woba_factors, vr_woba_factors, splits)

# Let's do some pitching now
calculate_pitching_stats(cards, vl_data, vr_data, splits)

# Analysis Sheet
generate_analysis_workbook(cards)

# Stats Sheet
generate_stats_workbook(ovr_data, vl_data, vr_data)
# End Stats Sheet

print(time.process_time() - start, "elapsed seconds")