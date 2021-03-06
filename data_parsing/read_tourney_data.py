from data_parsing.league_levels import tourney_mode_levels
from data_parsing.individual_player import read_individual_player, merge_player_data
from output_utils.progress.progress_bar import ProgressBar

import os
import copy

def get_stats_from_db_tourney(level_match, tourney_cards):
    player_stats = {}
    db = _read_files_tourney(tourney_cards)
    for level in db:
        if tourney_mode_levels[level] == tourney_mode_levels[level_match]:
            continue
        for league in db[level]:
            league_stats = db[level][league]
            for player in league_stats:
                cid = str(player["t_CID"])
                if cid in player_stats:
                    player_stats[cid] = merge_player_data(player_stats[cid], player)
                else:
                    player_stats[cid] = copy.deepcopy(player)
    return player_stats

def _read_files_tourney(cards):
    file_names = _get_matching_file_names()
    player_ratings = {}
    for card in cards:
        player_ratings[str(card["t_CID"])] = card

    db = {}
    column_names = []
    progress_bar = ProgressBar(len(file_names), "Reading tourney files")
    for file_name in file_names:
        progress_bar.update("reading " + file_name)
        f_name = file_name.split('/')[-1]
        file_name_split = f_name.split('_')
        level = file_name_split[0]
        file_n = file_name_split[1]
        if level not in db:
            db[level] = {}
        db[level][file_n] = []
        f = open(file_name, 'r')
        for line in f.readlines():
            if line.startswith("POS"):
                column_names = line.strip().split(",")
                continue
            player_info = line.strip().split(",")
            if player_info[0] == "":
                continue
            if len(player_info) < 4:
                continue
            cid = str(player_info[column_names.index("CID")])

            ovr = int(player_info[column_names.index("VAL")])
            # Live card not updated
            if cid in player_ratings:
                if player_ratings[cid]["ovr"] != ovr:
                    continue
            pd = read_individual_player(player_ratings[cid], player_info, column_names)
            if pd == None:
                continue
            if pd["games"] > 0 and pd["gamesstarted"] == 0:
                # RP
                # TODO fix SP as RP ratings
                if pd["pos"] == "SP":
                    continue
                db[level][file_n].append(pd)
            elif pd["games"] > 0 and pd["games"] == pd["gamesstarted"]:
                # SP
                # TODO fix RP as SP ratings
                if pd["pos"] == "RP":
                    continue
                db[level][file_n].append(pd)
            elif pd["pa"] > 0 or pd["bf"] > 0:
                # Batter
                db[level][file_n].append(pd)
        f.close()
        progress_bar.increment()
    return db

def _get_matching_file_names():
    files = os.listdir("data/tourney/")
    matching_names = []
    for file_name in files:
        matching_names.append("data/tourney/" + file_name)
    return matching_names