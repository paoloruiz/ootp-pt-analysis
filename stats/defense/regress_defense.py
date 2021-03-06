import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from util.number_utils import add_ip
import numpy as np
np.warnings.filterwarnings('ignore')

def regress_defensive_stats(player_data, position_ratings, outcome_stat):
    X_by_rating = {}
    y_by_rating = {}
    for player_info in player_data.values():
        if player_info["fieldingip"] < 5 or player_info[outcome_stat] == 0:
            continue
        ratings = [ ]
        for pr in position_ratings:
            ratings.append(player_info[pr])
        if player_info["t_CID"] not in X_by_rating:
            X_by_rating[player_info["t_CID"]] = ratings
            y_by_rating[player_info["t_CID"]] = [0.0, 0]
        y_by_rating[player_info["t_CID"]][0] += player_info[outcome_stat]
        y_by_rating[player_info["t_CID"]][1] += 1
    X = []
    y = []
    for cid in X_by_rating.keys():
        X.append(X_by_rating[cid])
        y.append(y_by_rating[cid][0] / y_by_rating[cid][1])
    
    reg_nnls = LinearRegression(fit_intercept=True, positive=True)
    reg_nnls.fit(X, y)
    r2 = reg_nnls.score(X, y)

    out = [ reg_nnls.intercept_ ]
    for i in range(len(position_ratings)):
        out.append(reg_nnls.coef_[i])

    return (out, r2)