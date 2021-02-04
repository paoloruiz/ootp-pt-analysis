import copy

def match_cids(player_db, player_ratings):
    _match_cids_player_ratings(player_db, player_ratings)
    unused = 0
    for player in player_ratings.values():
        if "used" not in player:
            unused += 1
            print(player["full_title"])
    print(unused, "unused")

def _match_cids_player_ratings(player_db, player_ratings):
    rp_players = []
    for i in range(len(player_db)):
        full_title = player_db[i]["full_title"]
        title_matches = list(filter(lambda x: x["full_title"].lower() == full_title.lower(), player_ratings.values()))

        if len(title_matches) == 0:
            continue
        elif len(title_matches) == 1:
            player_ratings[title_matches[0]["cid"]]["used"] = True
            continue
        elif len(title_matches) == 2:
            if title_matches[0]["cid"] in title_matches[1]["cid"] and "-rp" in title_matches[1]["cid"]:
                player_ratings[title_matches[0]["cid"]]["used"] = True
                player_ratings[title_matches[1]["cid"]]["used"] = True

                rp_player = copy.deepcopy(player_db[i])
                rp_player["t_CID"] = str(rp_player["t_CID"]) + "-rp"
                rp_player["stu"] = title_matches[1]["stu"]
                rp_player["stuVL"] = title_matches[1]["stuVL"]
                rp_player["stuVR"] = title_matches[1]["stuVR"]
                rp_players.append(rp_player)
                continue
            if title_matches[1]["cid"] in title_matches[0]["cid"] and "-rp" in title_matches[0]["cid"]:
                player_ratings[title_matches[0]["cid"]]["used"] = True
                player_ratings[title_matches[1]["cid"]]["used"] = True

                rp_player = copy.deepcopy(player_db[i])
                rp_player["t_CID"] = str(rp_player["t_CID"]) + "-rp"
                rp_player["stu"] = title_matches[0]["stu"]
                rp_player["stuVL"] = title_matches[0]["stuVL"]
                rp_player["stuVR"] = title_matches[0]["stuVR"]
                rp_players.append(rp_player)
                continue
            if title_matches[0]["cid"] in title_matches[1]["cid"] and "-sp" in title_matches[1]["cid"]:
                player_ratings[title_matches[0]["cid"]]["used"] = True
                player_ratings[title_matches[1]["cid"]]["used"] = True

                rp_player = copy.deepcopy(player_db[i])
                rp_player["t_CID"] = str(rp_player["t_CID"]) + "-sp"
                rp_player["stu"] = title_matches[1]["stu"]
                rp_player["stuVL"] = title_matches[1]["stuVL"]
                rp_player["stuVR"] = title_matches[1]["stuVR"]
                rp_players.append(rp_player)
                continue
            if title_matches[1]["cid"] in title_matches[0]["cid"] and "-sp" in title_matches[0]["cid"]:
                player_ratings[title_matches[0]["cid"]]["used"] = True
                player_ratings[title_matches[1]["cid"]]["used"] = True

                rp_player = copy.deepcopy(player_db[i])
                rp_player["t_CID"] = str(rp_player["t_CID"]) + "-sp"
                rp_player["stu"] = title_matches[0]["stu"]
                rp_player["stuVL"] = title_matches[0]["stuVL"]
                rp_player["stuVR"] = title_matches[0]["stuVR"]
                rp_players.append(rp_player)
                continue
    player_db.extend(rp_players)