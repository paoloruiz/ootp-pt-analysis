import statsmodels.api as sm

def regress_pitchers(
    player_data, 
    rating,
    get_rating_outcome_stat, 
    get_true_bf_stat, 
    hand,
    modifier
):
    outcomes_by_rating_and_hand = {}
    for player_info in player_data.values():
        if get_true_bf_stat(player_info) < 15:
            continue
        if player_info["throws"] == hand:
            rating_key = player_info[rating + modifier]
            if rating_key in outcomes_by_rating_and_hand:
                outcomes_by_rating_and_hand[rating_key] = (get_rating_outcome_stat(player_info) + outcomes_by_rating_and_hand[rating_key][0], get_true_bf_stat(player_info) + outcomes_by_rating_and_hand[rating_key][1])
            else:
                outcomes_by_rating_and_hand[rating_key] = (get_rating_outcome_stat(player_info), get_true_bf_stat(player_info))

    X = []
    y = []
    for rkey, value in outcomes_by_rating_and_hand.items():
        if value[1] == 0:
            continue
        X.append([ rkey ])
        y.append(value[0] / value[1])
    # initial attempt - we still need to throw out outliers
    model = sm.OLS(y, sm.add_constant(X))
    results = model.fit()
    influence = results.get_influence()
    cooks_distance = influence.cooks_distance[0]
    cutoff = 4.0 / ((len(X) - 2) if len(X) > 3 else 1)

    old_len_X = len(X)
    X = []
    y = []
    i = 0
    for rkey, value in outcomes_by_rating_and_hand.items():
        if cooks_distance[i] < cutoff or old_len_X < 4:
            X.append([ rkey ])
            y.append(value[0] / value[1])
        i += 1
    # Real prediction
    model = sm.OLS(y, sm.add_constant(X))
    results = model.fit()

    return ( results.params, results.rsquared )