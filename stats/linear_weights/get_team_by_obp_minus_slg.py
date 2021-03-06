import math
from stats.linear_weights.get_base_stats import getBaseStats

def _get_slg_minus_obp(x):
    return x["slg_minus_obp"]

def getTeams(player_data):
    possible_teams = []
    for year_league_team in player_data:
        if len(player_data[year_league_team]) < 24:
            continue
        basestats = getBaseStats(player_data[year_league_team])
        possible_teams.append({
            "slg_minus_obp": basestats["sluggingaverage"] - basestats["onbasepercentage"],
            "players": player_data[year_league_team]
        })
    possible_teams.sort(key=_get_slg_minus_obp)

    high_obp_index = math.floor(len(possible_teams) * 0.1)
    high_slg_index = math.floor(len(possible_teams) * 0.9)

    return (possible_teams[high_obp_index - 3:high_obp_index + 3], possible_teams[high_slg_index - 3:high_slg_index + 3])