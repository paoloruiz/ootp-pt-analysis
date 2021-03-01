from stats.hitting.hitting_factors import get_factors
from util.number_utils import min_max
from output_utils.progress.progress_bar import ProgressBar

def calculate_hitting_stats(cards, vl_data, vr_data, ovr_woba_factors, vl_woba_factors, vr_woba_factors, splits, hbp_rate):
    hitting_factors = get_factors(vl_data, vr_data)

    progress_bar = ProgressBar(len(cards), "Calculate batting projections")
    for card in cards:
        factors = hitting_factors["VL"][card["bats"]]
        _set_projections(card, factors, vl_woba_factors, "vL", hbp_rate)

        factors = hitting_factors["VR"][card["bats"]]
        _set_projections(card, factors, vr_woba_factors, "vR", hbp_rate)

        _set_ovr_projections(card, splits)

        progress_bar.increment()

    progress_bar.finish()
    print()

def _set_projections(card, factors, woba_factors, mod, hbp_rate):
    tot_pas = 720
    hbp = tot_pas * hbp_rate[card["t_CID"]] if card["t_CID"] in hbp_rate else 3
    bb = min_max(0, factors["eye"](card) * (tot_pas - hbp), tot_pas - hbp)
    k = min_max(0, factors["avk"](card) * (tot_pas - bb - hbp), tot_pas - bb - hbp)
    hr = min_max(0, factors["pow"](card) * (tot_pas - bb - k - hbp), tot_pas - bb - k - hbp)
    hits = min_max(0, factors["babip"](card) * (tot_pas - bb - k - hr - hbp), tot_pas - bb - k - hr - hbp)
    xbh = min_max(0, factors["gap"](card) * hits, hits)
    triples = min_max(0, factors["spe"](card) * xbh, xbh)
    doubles = xbh - triples
    singles = hits - xbh
    avg = (hits + hr) / (tot_pas - bb - hbp)
    obp = (hits + hr + bb + hbp) / tot_pas
    ops = obp + (singles + doubles * 2 + triples * 3 + hr * 4) / (tot_pas - hbp - bb)
    woba = (
        woba_factors["hbp_factor"] * hbp 
            + woba_factors["walks_factor"] * bb 
            + woba_factors["singles_factor"] * singles 
            + woba_factors["doubles_factor"] * doubles 
            + woba_factors["triples_factor"] * triples 
            + woba_factors["homeruns_factor"] * hr
        ) / tot_pas

    card["HBP_" + mod] = 3
    card["BB_" + mod] = bb
    card["K_" + mod] = k
    card["HR_" + mod] = hr
    card["singles_" + mod] = singles
    card["doubles_" + mod] = doubles
    card["triples_" + mod] = triples
    card["AVG_" + mod] = avg
    card["OBP_" + mod] = obp
    card["OPS_" + mod] = ops
    card["wOBA_" + mod] = woba

def _set_ovr_projections(card, splits):
    position = "catcher" if card["position"] == "C" else "fielder"
    ft_vr_split = splits["FT"]["vR%"][position]
    vr_vr_split = splits["vR"]["vR%"][position]
    vl_vr_split = splits["vL"]["vR%"][position]

    card["wOBA_ft_starter"] = card["wOBA_vL"] * (1 - ft_vr_split) + card["wOBA_vR"] * ft_vr_split
    card["wOBA_vR_starter"] = card["wOBA_vL"] * (1 - vr_vr_split) + card["wOBA_vR"] * vr_vr_split
    card["wOBA_vL_starter"] = card["wOBA_vL"] * (1 - vl_vr_split) + card["wOBA_vR"] * vl_vr_split
    pass