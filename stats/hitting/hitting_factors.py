from stats.hitting.regress_batting import regress_batters
from output_utils.progress.progress_bar import ProgressBar

def get_factors(vl_data, vr_data):
    hitting_factors = {
        "VL": {
            "S": {},
            "R": {},
            "L": {}
        },
        "VR": {
            "S": {},
            "R": {},
            "L": {}
        }
    }

    batter_data = [ vl_data, vr_data ]
    batter_types = [ "VL", "VR" ]
    ratings = [
        ("eye", lambda pi: pi["walks"], lambda pi: pi["pa"] - pi["timeshitbypitch"], lambda pi: pi["pa"] < 15, False),
        ("avk", lambda pi: pi["strikeouts"], lambda pi: pi["ab"] - pi["timeshitbypitch"], lambda pi: pi["ab"] < 10, False),
        ("pow", lambda pi: pi["homeruns"], lambda pi: pi["ab"] - pi["strikeouts"], lambda pi: pi["ab"] < 25, False),
        ("babip", lambda pi: pi["hits"] - pi["homeruns"], lambda pi: pi["ab"] - pi["strikeouts"] - pi["homeruns"], lambda pi: pi["hits"] < 10, False),
        ("gap", lambda pi: pi["doubles"] + pi["triples"], lambda pi: pi["hits"] - pi["homeruns"], lambda pi: (pi["doubles"] + pi["triples"]) < 1 or (pi["doubles"] + pi["triples"] > (pi["hits"] - pi["homeruns"])), False),
        ("spe", lambda pi: pi["triples"], lambda pi: pi["doubles"] + pi["triples"], lambda pi: pi["doubles"] + pi["triples"] < 5, True)
    ]
    hands = [ "R", "L", "S" ]

    progress_bar = ProgressBar(len(batter_data) * len(batter_types) * len(ratings), "Regressing batter factors")

    r_squareds = []
    for data in batter_data:
        for batter_type in batter_types:
            for rating, get_val, get_true_pa, should_sieve, skip_hands in ratings:
                if skip_hands:
                    hf_fun, r_squared_text = regress_batters(data, rating, get_val, get_true_pa, should_sieve, "ZZ", batter_type)
                    hitting_factors[batter_type]["S"][rating] = hf_fun
                    hitting_factors[batter_type]["R"][rating] = hf_fun
                    hitting_factors[batter_type]["L"][rating] = hf_fun
                    r_squareds.append(r_squared_text)
                else:
                    for hand in hands:
                        hf_fun, r_squared_text = regress_batters(data, rating, get_val, get_true_pa, should_sieve, hand, batter_type)
                        hitting_factors[batter_type][hand][rating] = hf_fun
                        r_squareds.append(r_squared_text)
                progress_bar.increment()
    progress_bar.finish()
    for r_squared_text in r_squareds:
        print(r_squared_text)
    print()
    return hitting_factors