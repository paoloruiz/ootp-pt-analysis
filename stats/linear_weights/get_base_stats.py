from util.number_utils import add_ip

def _new_tot_stats():
    return {
        "gamesplayed": 0,
        "atbats": 0,
        "plateappearances": 0,
        "hits": 0,
        "singles": 0,
        "doubles": 0,
        "triples": 0,
        "homeruns": 0,
        "runsscored": 0,
        "runsbattedin": 0,
        "walks": 0,
        "intentionalwalks": 0,
        "strikeouts": 0,
        "hitbypitch": 0,
        "sacflies": 0,
        "sacbunts": 0,
        "gidp": 0,
        "stolenbases": 0,
        "caughtstealing": 0,
        "gamesstartedtot": 0,
        "inningspitched": 0,
        "outs": 0
    }

# player_data - regular data pull
def getBaseStats(player_data):
    tot_stats = _new_tot_stats()
    _get_base_stats_inner(player_data, tot_stats)
    return tot_stats

def getBaseStatsByTeams(teams):
    tot_stats = _new_tot_stats()
    for team in teams:
        _get_base_stats_inner(team["players"], tot_stats)

    return tot_stats

def _get_base_stats_inner(player_data, tot_stats):
    for player in player_data.values():
        tot_stats["gamesplayed"] += player["g"]
        tot_stats["atbats"] += player["ab"]
        tot_stats["plateappearances"] += player["pa"]
        tot_stats["hits"] += player["hits"]
        tot_stats["singles"] += player["hits"] - (player["homeruns"] + player["doubles"] + player["triples"])
        tot_stats["doubles"] += player["doubles"]
        tot_stats["triples"] += player["triples"]
        tot_stats["homeruns"] += player["homeruns"]
        tot_stats["runsscored"] += player["runsscored"]
        tot_stats["runsbattedin"] += player["rbi"]
        tot_stats["walks"] += player["walks"]
        tot_stats["intentionalwalks"] += player["intentionallywalked"]
        tot_stats["strikeouts"] += player["strikeouts"]
        tot_stats["hitbypitch"] += player["timeshitbypitch"]
        tot_stats["sacflies"] += player["sacflies"]
        tot_stats["sacbunts"] + player["sacbunts"]
        tot_stats["gidp"] += player["gidp"]
        tot_stats["stolenbases"] += player["stolenbases"]
        tot_stats["caughtstealing"] += player["caughtstealing"]
        tot_stats["gamesstartedtot"] += player["gs"]
        tot_stats["outs"] += player["ab"] - player["hits"] + player["gidp"] + player["caughtstealing"]
        tot_stats["inningspitched"] = add_ip(add_ip(player["sp_ip"], tot_stats["inningspitched"]), player["rp_ip"])
    tot_stats["gamesstarted"] = tot_stats["gamesstartedtot"] / 9
    tot_stats["average"] = tot_stats["hits"] / tot_stats["atbats"]
    tot_stats["onbasepercentage"] = (tot_stats["hits"] + tot_stats["walks"] + tot_stats["hitbypitch"]) / (tot_stats["atbats"] + tot_stats["walks"] + tot_stats["hitbypitch"] + tot_stats["sacflies"])
    tot_stats["sluggingaverage"] = (tot_stats["singles"] + tot_stats["doubles"] * 2 + tot_stats["triples"] * 3 + tot_stats["homeruns"] * 4) / tot_stats["atbats"]
