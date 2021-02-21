import statsmodels.api as sm

def regress_batters(
    player_data, 
    rating, 
    get_rating_outcome_stat, 
    get_true_pa_stat, 
    should_sieve_pa,
    hand,
    modifier
):
    outcomes_by_rating_and_hand = {}
    for player_info in player_data.values():
        if should_sieve_pa(player_info):
            continue
        if player_info["bats"] == hand or hand == "ZZ":
            mod = modifier if hand != "ZZ" else ""
            rating_key = player_info[rating + mod]
            if rating_key in outcomes_by_rating_and_hand:
                outcomes_by_rating_and_hand[rating_key] = (get_rating_outcome_stat(player_info) + outcomes_by_rating_and_hand[rating_key][0], get_true_pa_stat(player_info) + outcomes_by_rating_and_hand[rating_key][1])
            else:
                outcomes_by_rating_and_hand[rating_key] = (get_rating_outcome_stat(player_info), get_true_pa_stat(player_info))

    X = []
    y = []
    for rkey, value in outcomes_by_rating_and_hand.items():
        X.append([ rkey ])
        y.append(value[0] / value[1])
    # initial attempt - we still need to throw out outliers
    model = sm.OLS(y, sm.add_constant(X))
    results = model.fit()
    influence = results.get_influence()
    cooks_distance = influence.cooks_distance[0]
    cutoff = 4.0 / (len(X) - 2)

    X = []
    y = []
    i = 0
    for rkey, value in outcomes_by_rating_and_hand.items():
        if cooks_distance[i] < cutoff:
            X.append([ rkey ])
            y.append(value[0] / value[1])
        i += 1
    # Real prediction
    model = sm.OLS(y, sm.add_constant(X))
    results = model.fit()

    handed_text = "Lefty " if hand == "L" else "Righty " if hand == "R" else "Switch " if hand != "ZZ" else ""
    r_squared_text = handed_text + modifier + " " + rating + " r^2: " + str(results.rsquared)
    return (lambda pi: pi[rating] * results.params[1] + results.params[0], r_squared_text)