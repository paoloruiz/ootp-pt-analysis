import statsmodels.api as sm

def get_woba_factors(ovr_data, vl_data, vr_data):
    ovr_factors = _calc_woba_factors(ovr_data)
    vl_factors = _calc_woba_factors(vl_data)
    vr_factors = _calc_woba_factors(vr_data)
    # Printing so we can check our r^2 values. Should be high
    print("Ovr wOBA r^2 factor:", ovr_factors["r_2"], "vL wOBA r^2 factor:", vl_factors["r_2"], "vR wOBA r^2 factor:", vr_factors["r_2"])
    return (ovr_factors, vl_factors, vr_factors)

def _calc_woba_factors(player_data):
    X = []
    y = []
    pa = 0
    walks = 0
    hbp = 0
    singles = 0
    doubles = 0
    triples = 0
    homeruns = 0
    ibb = 0
    for player in player_data.values():
        pa += player["pa"]
        walks += player["walks"]
        hbp += player["timeshitbypitch"]
        singles += player["hits"] - (player["homeruns"] + player["doubles"] + player["triples"])
        doubles += player["doubles"]
        triples += player["triples"]
        homeruns += player["homeruns"]
        ibb += player["intentionallywalked"]
        if player["pa"] < 20:
            continue
        X.append([ 1, player["walks"], player["timeshitbypitch"], player["hits"] - (player["homeruns"] + player["doubles"] + player["triples"]), player["doubles"], player["triples"], player["homeruns"] ])
        y.append(player["woba"] * (player["pa"] - player["intentionallywalked"]))

    results = sm.OLS(y, X).fit()

    avg_woba = (results.params[0] + results.params[1] * walks + results.params[2] * hbp + results.params[3] * singles + results.params[4] * doubles + results.params[5] * triples + results.params[6] * homeruns) / (pa - ibb)
    return {
        "lg_woba": avg_woba,
        "woba_scale": results.params[0],
        "walks_factor": results.params[1],
        "hbp_factor": results.params[2],
        "singles_factor": results.params[3],
        "doubles_factor": results.params[4],
        "triples_factor": results.params[5],
        "homeruns_factor": results.params[6],
        "r_2": results.rsquared
    }

