import statsmodels.api as sm

def regress_steal_attempts(player_data):
    outcome_by_rating = {}
    for player_info in player_data.values():
        if player_info["bsrunchances"] < 10:
            continue
        if player_info["spe"] not in outcome_by_rating:
            outcome_by_rating[player_info["spe"]] = [0.0, 0]
        outcome_by_rating[player_info["spe"]][0] += player_info["stolenbases"] + player_info["caughtstealing"]
        outcome_by_rating[player_info["spe"]][1] += player_info["bsrunchances"]

    X = []
    y = []
    for rkey, y_by_rating in outcome_by_rating.items():
        X.append([ rkey ])
        y.append(y_by_rating[0] / y_by_rating[1])
    # initial attempt - we still need to throw out outliers
    model = sm.OLS(y, sm.add_constant(X))
    results = model.fit()
    influence = results.get_influence()
    cooks_distance = influence.cooks_distance[0]
    cutoff = 4.0 / (len(X) - 2)

    X = []
    y = []
    i = 0
    for rkey, y_by_rating in outcome_by_rating.items():
        if cooks_distance[i] < cutoff:
            X.append([ rkey ])
            y.append(y_by_rating[0] / y_by_rating[1])
        i += 1
    # Real prediction
    model = sm.OLS(y, sm.add_constant(X))
    results = model.fit()
    
    return [ results.params, results.rsquared ]

def regress_success_rate(player_data):
    outcome_by_rating = {}
    for player_info in player_data.values():
        if player_info["stolenbases"] + player_info["caughtstealing"] < 5:
            continue
        if player_info["ste"] not in outcome_by_rating:
            outcome_by_rating[player_info["ste"]] = [0.0, 0]
        outcome_by_rating[player_info["ste"]][0] += player_info["stolenbases"]
        outcome_by_rating[player_info["ste"]][1] += player_info["stolenbases"] + player_info["caughtstealing"]

    X = []
    y = []
    for rkey, y_by_rating in outcome_by_rating.items():
        X.append([ rkey ])
        y.append(y_by_rating[0] / y_by_rating[1])
    # initial attempt - we still need to throw out outliers
    model = sm.OLS(y, sm.add_constant(X))
    results = model.fit()
    influence = results.get_influence()
    cooks_distance = influence.cooks_distance[0]
    cutoff = 4.0 / (len(X) - 2)

    X = []
    y = []
    i = 0
    for rkey, y_by_rating in outcome_by_rating.items():
        if cooks_distance[i] < cutoff:
            X.append([ rkey ])
            y.append(y_by_rating[0] / y_by_rating[1])
        i += 1
    # Real prediction
    model = sm.OLS(y, sm.add_constant(X))
    results = model.fit()
    
    return [ results.params, results.rsquared ]

def regress_ubr(player_data):
    outcome_by_rating = {}
    for player_info in player_data.values():
        if player_info["bsrunchances"] < 10:
            continue
        if player_info["run"] not in outcome_by_rating:
            outcome_by_rating[player_info["run"]] = [0.0, 0.0]
        outcome_by_rating[player_info["run"]][0] += player_info["ubr"]
        outcome_by_rating[player_info["run"]][1] += player_info["bsrunchances"]

    X = []
    y = []
    for rkey, y_by_rating in outcome_by_rating.items():
        X.append([ rkey ])
        y.append(y_by_rating[0] / y_by_rating[1])
    # initial attempt - we still need to throw out outliers
    model = sm.OLS(y, sm.add_constant(X))
    results = model.fit()
    influence = results.get_influence()
    cooks_distance = influence.cooks_distance[0]
    cutoff = 4.0 / (len(X) - 2)

    X = []
    y = []
    i = 0
    for rkey, y_by_rating in outcome_by_rating.items():
        if cooks_distance[i] < cutoff:
            X.append([ rkey ])
            y.append(y_by_rating[0] / y_by_rating[1])
        i += 1
    # Real prediction
    model = sm.OLS(y, sm.add_constant(X))
    results = model.fit()
    
    return [ results.params, results.rsquared ]