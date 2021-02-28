from data_parsing.league_levels import pt_mode_levels
from data_parsing.individual_player import read_individual_player, merge_player_data
from output_utils.progress.progress_bar import ProgressBar
import os

# Cards removed from packs and therefore no longer in database
known_missing_cids = [
    "16661", # Sam Tuivailala 71
]

def read_files_to_db(min_level, min_year, player_data):
    player_ratings_db = {}
    for card in player_data:
        player_ratings_db[str(card["CID"])] = card
    ovr_data, ovr_data_ylt = _read_files(_get_matching_file_names("data/overall/", min_level, min_year), player_ratings_db, "Ovr")
    vl_data, vl_data_ylt = _read_files(_get_matching_file_names("data/vL/", min_level, min_year), player_ratings_db, "vL")
    vr_data, vr_data_ylt = _read_files(_get_matching_file_names("data/vR/", min_level, min_year), player_ratings_db, "vR")
    print()
    return (ovr_data, vl_data, vr_data, ovr_data_ylt, vl_data_ylt, vr_data_ylt)

def _read_files(file_names, player_data, file_type_name):
    db = {}
    year_league_team_db = {}
    progress_bar = ProgressBar(len(file_names), "Reading " + file_type_name + " files")
    for file_name in file_names:
        progress_bar.update("Reading " + file_name)
        f = open(file_name, "r")
        file_name = file_name.split("/")[-1]
        file_name_split = file_name.split("_")
        year = int(file_name_split[0])
        league = file_name_split[1]
        column_names = []
        for line in f.readlines():
            if line.startswith("POS"):
                column_names = line.strip().split(",")
                continue
            player_info = line.strip().split(",")
            if player_info[0] == "":
                continue
            if len(player_info) < 4:
                continue
            cid = player_info[column_names.index("CID")]
            name = player_info[column_names.index("Name")]
            ovr = int(player_info[column_names.index("VAL")])
            if cid in player_data and player_data[cid]["ovr"] != ovr:
                # This is generally the case for live cards whose ratings have changed
                continue
            player_rating = _match_player(cid, player_data)
            if player_rating == None:
                if str(cid) not in known_missing_cids:
                    print("No players found to match cid: ", cid, " with name: ", name, " and ovr: ", ovr)
                continue
            new_player_info = read_individual_player(player_rating, player_info, column_names)
            if new_player_info == None:
                continue

            # Add in stuff to analyse by individual team
            year_league_team = str(year) + league + new_player_info["team"]
            if year_league_team not in year_league_team_db:
                year_league_team_db[year_league_team] = {}
            year_league_team_db[year_league_team][new_player_info["t_CID"]] = new_player_info

            if cid in db:
                db[cid] = merge_player_data(db[cid], new_player_info)
            else:
                db[cid] = new_player_info
        f.close()

        progress_bar.increment("Reading " + file_name)
    progress_bar.finish()
    return db, year_league_team_db

def _match_player(cid, player_data):
    # TODO -sp/-rp stuff here
    if str(cid) in player_data:
        return player_data[str(cid)]
    return None

def _get_matching_file_names(folder, min_level, min_year):
    files = os.listdir(folder)
    matching_names = []
    for file_name in files:
        # Read each individual part of a file name
        file_name_split = file_name.replace(".csv", "").split("_")
        # Throw out files that don't match the proper naming scheme
        if len(file_name_split) < 3:
            continue
        year = int(file_name_split[0])
        # Exclude everything before our starting year
        if min_year > year:
            continue
        level = pt_mode_levels[file_name_split[1][:-3]]
        # Exclude every level below our min
        if pt_mode_levels[min_level] < level:
            continue

        matching_names.append(folder + file_name)
    return matching_names