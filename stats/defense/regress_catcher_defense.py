import statsmodels.api as sm
from util.number_utils import add_ip, ip_to_num

def regress_cera(player_data):
    X_by_rating = {}
    y_by_rating = {}
    for player_info in player_data.values():
        if player_info["fieldingip"] < 5 or player_info["cera"] < 2.0:
            continue
        ratings = [ 1, player_info["cabi"] ]
        if player_info["t_CID"] not in X_by_rating:
            X_by_rating[player_info["t_CID"]] = ratings
            y_by_rating[player_info["t_CID"]] = [0.0, 0]
        # TODO could weight CERA by ip when doing regression
        y_by_rating[player_info["t_CID"]][0] += player_info["cera"]
        y_by_rating[player_info["t_CID"]][1] += 1
        
    X = []
    y = []
    for cid in X_by_rating.keys():
        X.append(X_by_rating[cid])
        y.append(y_by_rating[cid][0] / y_by_rating[cid][1])
    
    model = sm.OLS(y, X)
    results = model.fit()
    influence = results.get_influence()
    cooks_distance = influence.cooks_distance[0]
    cutoff = 4.0 / ((len(X) - 2) if len(X) > 3 else 1)

    old_len_X = len(X)
    X_filtered = []
    y_filtered = []
    i = 0
    for i in range(len(X)):
        if cooks_distance[i] < cutoff or old_len_X < 4:
            X_filtered.append(X[i])
            y_filtered.append(y[i])
    # Real prediction
    model = sm.OLS(y_filtered, X_filtered)
    results = model.fit()

    return (results.params, results.rsquared)

def regress_rto(player_data):
    avg_cabi = 0.0
    avg_carm = 0.0
    avg_ip = 0.0
    attempts_by_arm = {}
    rto_by_arm = {}
    for player_info in player_data.values():
        if player_info["runnersthrownout"] < 1 or player_info["cera"] < 2.0 or player_info["carm"] < 15 or player_info["fieldingip"] < 10.0:
            continue

        carm = player_info["carm"]
        cabi = player_info["cabi"]
        avg_carm = (avg_carm * avg_ip + carm * ip_to_num(player_info["fieldingip"])) / (avg_ip + ip_to_num(player_info["fieldingip"]))
        avg_cabi = (avg_cabi * avg_ip + cabi * ip_to_num(player_info["fieldingip"])) / (avg_ip + ip_to_num(player_info["fieldingip"]))
        avg_ip += ip_to_num(player_info["fieldingip"])

        if carm in attempts_by_arm:
            attempts_by_arm[carm] = (player_info["stolenbaseattempts"] + attempts_by_arm[carm][0], add_ip(player_info["fieldingip"], attempts_by_arm[carm][1]))
            rto_by_arm[carm] = (player_info["runnersthrownout"] + rto_by_arm[carm][0], player_info["stolenbaseattempts"] + rto_by_arm[carm][1])
        else:
            attempts_by_arm[carm] = (player_info["stolenbaseattempts"], player_info["fieldingip"])
            rto_by_arm[carm] = (player_info["runnersthrownout"], player_info["stolenbaseattempts"])

    X = []
    y = []
    for carm in attempts_by_arm:
        if attempts_by_arm[carm][1] == 0:
            continue
        X.append(carm)
        y.append(attempts_by_arm[carm][0] / attempts_by_arm[carm][1])
    # initial attempt - we still need to throw out outliers
    att_model = sm.OLS(y, sm.add_constant(X))
    att_results = att_model.fit()
    att_influence = att_results.get_influence()
    att_cooks_distance = att_influence.cooks_distance[0]
    att_cutoff = 4.0 / ((len(X) - 2) if len(X) > 3 else 1)

    att_old_len_X = len(X)
    X = []
    y = []
    i = 0
    for carm in attempts_by_arm:
        if att_cooks_distance[i] < att_cutoff or att_old_len_X < 4:
            X.append(carm)
            y.append(attempts_by_arm[carm][0] / attempts_by_arm[carm][1])
        i += 1
    # Real prediction
    att_model = sm.OLS(y, sm.add_constant(X))
    att_results = att_model.fit()
    X = []
    y = []
    for carm in attempts_by_arm:
        if attempts_by_arm[carm][1] == 0:
            continue
        X.append(carm)
        y.append(rto_by_arm[carm][0] / rto_by_arm[carm][1])

    # initial attempt - we still need to throw out outliers
    rto_model = sm.OLS(y, sm.add_constant(X))
    rto_results = rto_model.fit()
    rto_influence = rto_results.get_influence()
    rto_cooks_distance = rto_influence.cooks_distance[0]
    rto_cutoff = 4.0 / ((len(X) - 2) if len(X) > 3 else 1)

    rto_old_len_X = len(X)
    X = []
    y = []
    i = 0
    for carm in attempts_by_arm:
        if rto_cooks_distance[i] < rto_cutoff or rto_old_len_X < 4:
            X.append(carm)
            y.append(rto_by_arm[carm][0] / rto_by_arm[carm][1])
        i += 1
    # Real prediction
    rto_model = sm.OLS(y, sm.add_constant(X))
    rto_results = rto_model.fit()

    # attempts by arm, r2, rto/att by arm, r2
    return (att_results.params, att_results.rsquared, rto_results.params, rto_results.rsquared, avg_carm, avg_cabi)