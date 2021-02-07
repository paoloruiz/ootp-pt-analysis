import statsmodels.api as sm

def calculate_babips(cards):
    matrix = _get_babip_matrix()
    for card in cards:
        _get_babip(matrix, card)

def _get_babip_matrix():
    stats = {}

    f = open('data/babcalc.csv', 'r')
    for line in f.readlines():
        if line.startswith("CON"):
            continue
        data = line.strip().split(",")
        babip = int(data[2])
        power = int(data[3])
        avk = int(data[4])
        con = int(data[0])

        # Read into each category
        b_i = "low_bab;"
        if babip > 50:
            b_i = "hi_bab;"
        p_i = "low_pow;"
        if power > 11:
            p_i = "midlow_pow;"
        if power > 50:
            p_i = "midhi_pow;"
        if power > 110:
            p_i = "hi_pow;"
        a_i = "low_avk"
        if avk > 11:
            a_i = "mid_avk"
        if avk > 50:
            a_i = "hi_avk"

        indic = b_i + p_i + a_i

        if indic not in stats:
            stats[indic] = []
        
        stats[indic].append((con, [ babip, power, avk, 1 ]))
    f.close()

    out = {}
    # For each category, run a regression
    for k in stats.keys():
        X = []
        y = []
        for statline in stats[k]:
            X.append(statline[1])
            y.append(statline[0])

        model = sm.OLS(y, X)
        results = model.fit()
        if results.rsquared < 0.99:
            # Not great in these categories, may need to collect more data
            # print(k, results.rsquared)
            pass
        out[k] = [ *results.params ]
    return out

def _get_babip(matrix, player):
    vL_babip = _get_babip_inner(matrix, player["conVL"], player["powVL"], player["avkVL"])
    vR_babip = _get_babip_inner(matrix, player["conVR"], player["powVR"], player["avkVR"])
    player["babip"] = (vL_babip + vR_babip) / 2.0
    player["babipVL"] = vL_babip
    player["babipVR"] = vR_babip

def _get_babip_inner(matrix, con, power, avk):
    p_i = "low_pow;"
    if power > 11:
        p_i = "midlow_pow;"
    if power > 50:
        p_i = "midhi_pow;"
    if power > 110:
        p_i = "hi_pow;"

    a_i = "low_avk"
    if avk > 11:
        a_i = "mid_avk"
    if avk > 50:
        a_i = "hi_avk"

    high_bab_params = matrix["hi_bab;" + p_i + a_i]
    high_babip = (con - (power * high_bab_params[1]) - (avk * high_bab_params[2]) - high_bab_params[3]) / high_bab_params[0]

    low_bab_params = matrix["low_bab;" + p_i + a_i]
    low_babip = (con - (power * low_bab_params[1]) - (avk * low_bab_params[2]) - low_bab_params[3]) / low_bab_params[0]

    if high_babip > 50 and high_babip < 110:
        return high_babip
    if low_babip < 51 and low_babip > 0:
        return low_babip

    # Expand a little to see if near misses are close
    if high_babip < 51 and high_babip > 40:
        return high_babip

    if low_babip > 50 and low_babip < 60:
        return low_babip

    # Well if both are high, let's take the lower one.
    if high_babip > 110 and low_babip > 0:
        return low_babip

    return high_babip