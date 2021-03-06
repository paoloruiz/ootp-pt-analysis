import copy
# from sheet stuff
xb_rate_1outs_out_3b = 0.5
xb_rate_0outs_out_3b = 0.5
xb_rate_2outs_single_2b = 0.75
xb_rate_1outs_single_2b = 0.5
xb_rate_1outs_out_2b = 0.25
xb_rate_0outs_single_2b = 0.3
xb_rate_0outs_out_2b = 0.25
xb_rate_2outs_single_1b = 0.25
xb_rate_2outs_double_1b = 0.5
xb_rate_1outs_single_1b = 0.25
xb_rate_1outs_double_1b = 0.25
xb_rate_1outs_out_1b = 0.05
xb_rate_0outs_single_1b = 0.25
xb_rate_0outs_double_1b = 0.15
xb_rate_0outs_out_1b = 0.05

def calcLinWts(basestats, linwts_type, csv_writer):
    # All from the sheet on https://blogs.fangraphs.com/team-specific-hitter-values-by-markov/
    valPA = basestats["atbats"] + basestats["walks"] + basestats["hitbypitch"]
    valTOB = basestats["hits"] + basestats["walks"] + basestats["hitbypitch"]
    # Originally 0.037 on sheet
    out_on_bases_rate = (basestats["caughtstealing"] + basestats["gidp"]) / (basestats["singles"] + basestats["walks"] + basestats["hitbypitch"])

    names = []
    vals = []

    freq_stats = _gen_freqency_stats(basestats, valPA, valTOB, out_on_bases_rate, 0, "")

    orig_weights = _markov_chain(freq_stats)

    pebble = freq_stats["freqPA"] / 100

    pebble_valPA = basestats["atbats"] + (pebble + basestats["walks"] + basestats["hitbypitch"])
    pebble_valTOB = basestats["hits"] + (pebble + basestats["walks"] + basestats["hitbypitch"])

    bb_freq_stats = _gen_freqency_stats(basestats, pebble_valPA, pebble_valTOB, out_on_bases_rate, pebble, "bb")
    bb_weights = _markov_chain(bb_freq_stats)
    bb_lwts = (bb_weights["runsAll"] - orig_weights["runsAll"]) / (bb_freq_stats["freqPA"] - freq_stats["freqPA"])

    singles_freq_stats = _gen_freqency_stats(basestats, pebble_valPA, pebble_valTOB, out_on_bases_rate, pebble, "1b")
    singles_weights = _markov_chain(singles_freq_stats)
    singles_lwts = (singles_weights["runsAll"] - orig_weights["runsAll"]) / (singles_freq_stats["freqPA"] - freq_stats["freqPA"])

    doubles_freq_stats = _gen_freqency_stats(basestats, pebble_valPA, pebble_valTOB, out_on_bases_rate, pebble, "2b")
    doubles_weights = _markov_chain(doubles_freq_stats)
    doubles_lwts = (doubles_weights["runsAll"] - orig_weights["runsAll"]) / (doubles_freq_stats["freqPA"] - freq_stats["freqPA"])

    triples_freq_stats = _gen_freqency_stats(basestats, pebble_valPA, pebble_valTOB, out_on_bases_rate, pebble, "3b")
    triples_weights = _markov_chain(triples_freq_stats)
    triples_lwts = (triples_weights["runsAll"] - orig_weights["runsAll"]) / (triples_freq_stats["freqPA"] - freq_stats["freqPA"])

    homeruns_freq_stats = _gen_freqency_stats(basestats, pebble_valPA, pebble_valTOB, out_on_bases_rate, pebble, "hr")
    homeruns_weights = _markov_chain(homeruns_freq_stats)
    homeruns_lwts = (homeruns_weights["runsAll"] - orig_weights["runsAll"]) / (homeruns_freq_stats["freqPA"] - freq_stats["freqPA"])

    strikeout_freq_stats = _gen_freqency_stats(basestats, valPA, valTOB, out_on_bases_rate, pebble, "so")
    strikeouts_weights = _markov_chain(strikeout_freq_stats)
    strikeouts_lwts = (strikeouts_weights["runsAll"] - orig_weights["runsAll"]) / pebble

    outs_lwts = -1 * (freq_stats["freqBBandHBP"] * bb_lwts + freq_stats["freq1B"] * singles_lwts + freq_stats["freq2B"] * doubles_lwts + freq_stats["freq3B"] * triples_lwts 
                    + freq_stats["freqHR"] * homeruns_lwts + freq_stats["freqSO"] * strikeouts_lwts) / freq_stats["freqOUT"]

    tot_outs_lwts = outs_lwts + strikeouts_lwts

    lg_avg_woba = ((bb_lwts - tot_outs_lwts) * (basestats["walks"] + basestats["hitbypitch"]) + (singles_lwts - tot_outs_lwts) * basestats["singles"] 
                    + (doubles_lwts - tot_outs_lwts) * basestats["doubles"] + (triples_lwts - tot_outs_lwts) * basestats["triples"] 
                    + (homeruns_lwts - tot_outs_lwts) * basestats["homeruns"]) / (basestats["atbats"] + basestats["walks"] - basestats["intentionalwalks"] + basestats["sacflies"] + basestats["hitbypitch"])
    
    return {
        "lg_avg_wOBA": lg_avg_woba,
        "wOBA_scale": lg_avg_woba / basestats["onbasepercentage"],
        "bb_and_hbp_lwts": bb_lwts - tot_outs_lwts,
        "singles_lwts": singles_lwts - tot_outs_lwts,
        "doubles_lwts": doubles_lwts - tot_outs_lwts,
        "triples_lwts": triples_lwts - tot_outs_lwts,
        "homeruns_lwts": homeruns_lwts - tot_outs_lwts,
        "strikeout_lwts": strikeouts_lwts,
        "outs_lwts": outs_lwts,
        "so_and_outs_lwts": outs_lwts + strikeouts_lwts,
        "runSB": 0.2,
        "runCS": -1 * (2 * basestats["runsscored"] / basestats["outs"] + 0.075),
        "r_per_pa": basestats["runsscored"] / basestats["plateappearances"],
        "r_per_win": basestats["runsscored"] / basestats["inningspitched"] * 9 * 1.5 + 3
    }

def _gen_freqency_stats(basestats, valPA, valTOB, out_on_bases_rate, pebble, pebble_stat):
    freqOBP = valTOB / valPA
    freqOUT = 1.0 - freqOBP

    walks_pebble = pebble if pebble_stat == "bb" else 0
    singles_pebble = pebble if pebble_stat == "1b" else 0
    doubles_pebble = pebble if pebble_stat == "2b" else 0
    triples_pebble = pebble if pebble_stat == "3b" else 0
    homeruns_pebble = pebble if pebble_stat == "hr" else 0
    strikeouts_pebble = pebble if pebble_stat == "so" else 0

    freqBBandHBP = (basestats["walks"] + basestats["hitbypitch"] + walks_pebble) / valPA
    freq1B = (basestats["singles"] + singles_pebble) / valPA
    multihit_pebble_adjust = (doubles_pebble + triples_pebble + homeruns_pebble) / valPA
    return {
        "runspergs": basestats["runsscored"] / basestats["gamesstarted"],
        "valPA": valPA,
        "valTOB": valTOB,
        "freqOBP": freqOBP,
        "freqBBandHBP": freqBBandHBP,
        "freq1B": freq1B,
        "freq2B": (basestats["doubles"] + doubles_pebble) / valPA,
        "freq3B": (basestats["triples"] + triples_pebble) / valPA,
        "freqHR": (basestats["homeruns"] + homeruns_pebble) / valPA,
        "freqSO": (basestats["strikeouts"] + strikeouts_pebble) / valPA,
        "freqOUT": freqOUT,
        "freqPA": (freqOBP / freqOUT) * 27 + 27,
        "freqPArevised": ((freqOBP / freqOUT) * 27 + 27) * (1 - ((basestats["gidp"] + basestats["caughtstealing"]) / valPA + out_on_bases_rate * (freqBBandHBP + freq1B + multihit_pebble_adjust))),
        "rateNonKOut": 1.0 - ((basestats["strikeouts"] + strikeouts_pebble) / valPA) / freqOUT
    }

def _markov_chain(freq_stats):
    calculatedStats = {}
    calculatedStats["3b_2_2"] = freq_stats["freqOUT"]
    calculatedStats["3b_2_1"] = calculatedStats["3b_2_2"] * freq_stats["freqBBandHBP"] + freq_stats["freqOUT"]
    calculatedStats["3b_2_0"] = calculatedStats["3b_2_1"] * freq_stats["freqBBandHBP"] + freq_stats["freqOUT"]
    calculatedStats["3b_1_2"] = calculatedStats["3b_2_2"] * freq_stats["freqOUT"] * (1.0 - freq_stats["rateNonKOut"] * xb_rate_1outs_out_3b)
    calculatedStats["3b_1_1"] = calculatedStats["3b_1_2"] * freq_stats["freqBBandHBP"] + calculatedStats["3b_2_1"] * freq_stats["freqOUT"] * (1.0 - freq_stats["rateNonKOut"] * xb_rate_1outs_out_3b)
    calculatedStats["3b_1_0"] = calculatedStats["3b_1_1"] * freq_stats["freqBBandHBP"] + calculatedStats["3b_2_0"] * freq_stats["freqOUT"] * (1.0 - freq_stats["rateNonKOut"] * xb_rate_1outs_out_3b)
    calculatedStats["3b_0_2"] = calculatedStats["3b_1_2"] * freq_stats["freqOUT"] * (1.0 - freq_stats["rateNonKOut"] * xb_rate_0outs_out_3b)
    calculatedStats["3b_0_1"] = calculatedStats["3b_0_2"] * freq_stats["freqBBandHBP"] + calculatedStats["3b_1_1"] * freq_stats["freqOUT"] * (1.0 - freq_stats["rateNonKOut"] * xb_rate_0outs_out_3b)
    calculatedStats["3b_0_0"] = calculatedStats["3b_0_1"] * freq_stats["freqBBandHBP"] + calculatedStats["3b_1_0"] * freq_stats["freqOUT"] * (1.0 - freq_stats["rateNonKOut"] * xb_rate_0outs_out_3b)
    calculatedStats["2b_2_1"] = calculatedStats["3b_2_2"] * (freq_stats["freqBBandHBP"] + freq_stats["freq1B"] * (1.0 - xb_rate_2outs_single_2b)) + freq_stats["freqOUT"]
    calculatedStats["2b_2_0"] = calculatedStats["2b_2_1"] * freq_stats["freqBBandHBP"] + calculatedStats["3b_2_1"] * freq_stats["freq1B"] * (1.0 - xb_rate_2outs_single_2b) + freq_stats["freqOUT"]
    calculatedStats["2b_1_1"] = (calculatedStats["3b_1_2"] * (freq_stats["freqBBandHBP"] + freq_stats["freq1B"] * (1.0 - xb_rate_1outs_single_2b)) 
                                    + calculatedStats["3b_2_1"] * freq_stats["freqOUT"] * freq_stats["rateNonKOut"] * xb_rate_1outs_out_2b 
                                    + calculatedStats["2b_2_1"] * freq_stats["freqOUT"] * (1.0 - freq_stats["rateNonKOut"] * xb_rate_1outs_out_2b)) 
    calculatedStats["2b_1_0"] = (calculatedStats["2b_1_1"] * freq_stats["freqBBandHBP"] + calculatedStats["3b_1_1"] * freq_stats["freq1B"] * (1.0 - xb_rate_1outs_single_2b) 
                                    + calculatedStats["3b_2_0"] * freq_stats["freqOUT"] * freq_stats["rateNonKOut"] * xb_rate_1outs_out_2b 
                                    + calculatedStats["2b_2_0"] * freq_stats["freqOUT"] * (1.0 - freq_stats["rateNonKOut"] * xb_rate_1outs_out_2b))
    calculatedStats["2b_0_1"] = (calculatedStats["3b_0_2"] * (freq_stats["freqBBandHBP"] + freq_stats["freq1B"] * (1.0 - xb_rate_0outs_single_2b)) 
                                    + calculatedStats["3b_1_1"] * freq_stats["freqOUT"] * freq_stats["rateNonKOut"] * xb_rate_0outs_out_2b 
                                    + calculatedStats["2b_1_1"] * freq_stats["freqOUT"] * (1.0 - freq_stats["rateNonKOut"] * xb_rate_0outs_out_2b))
    calculatedStats["2b_0_0"] = (calculatedStats["2b_0_1"] * freq_stats["freqBBandHBP"] + calculatedStats["3b_0_1"] * freq_stats["freq1B"] * (1.0 - xb_rate_0outs_single_2b)
                                    + calculatedStats["3b_1_0"] * freq_stats["freqOUT"] * freq_stats["rateNonKOut"] * xb_rate_0outs_out_2b 
                                    + calculatedStats["2b_1_0"] * freq_stats["freqOUT"] * (1.0 - freq_stats["rateNonKOut"] * xb_rate_0outs_out_2b))
    calculatedStats["1b_2_0"] = (calculatedStats["2b_2_1"] * (freq_stats["freqBBandHBP"] + freq_stats["freq1B"] * (1.0 - xb_rate_2outs_single_1b)) 
                                    + calculatedStats["3b_2_1"] * (freq_stats["freq1B"] * xb_rate_2outs_single_1b + freq_stats["freq2B"] * (1.0 - xb_rate_2outs_double_1b)) 
                                    + freq_stats["freqOUT"])
    calculatedStats["1b_1_0"] = (calculatedStats["2b_1_1"] * (freq_stats["freqBBandHBP"] + freq_stats["freq1B"] * (1.0 - xb_rate_1outs_single_1b)) 
                                    + calculatedStats["3b_1_1"] * (freq_stats["freq1B"] * xb_rate_1outs_single_1b + freq_stats["freq2B"] * (1.0 - xb_rate_1outs_double_1b)) 
                                    + calculatedStats["2b_2_0"] * freq_stats["freqOUT"] * freq_stats["rateNonKOut"] * xb_rate_1outs_out_1b 
                                    + calculatedStats["1b_2_0"] * freq_stats["freqOUT"] * (1.0 - freq_stats["rateNonKOut"] * xb_rate_1outs_out_1b))
    calculatedStats["1b_0_0"] = (calculatedStats["2b_0_1"] * (freq_stats["freqBBandHBP"] + freq_stats["freq1B"] * (1.0 - xb_rate_0outs_single_1b)) 
                                    + calculatedStats["3b_0_1"] * (freq_stats["freq1B"] * xb_rate_0outs_single_1b + freq_stats["freq2B"] * (1.0 - xb_rate_0outs_double_1b)) 
                                    + calculatedStats["2b_1_0"] * freq_stats["freqOUT"] * freq_stats["rateNonKOut"] * xb_rate_0outs_out_1b 
                                    + calculatedStats["1b_1_0"] * freq_stats["freqOUT"] * (1.0 - freq_stats["rateNonKOut"] * xb_rate_0outs_out_1b))
    calculatedStats["chance3B_3"] = 1.0 - (calculatedStats["3b_2_0"] + calculatedStats["3b_1_0"] + calculatedStats["3b_0_0"]) / 3
    calculatedStats["chance2B_3"] = 1.0 - (calculatedStats["2b_2_0"] + calculatedStats["2b_1_0"] + calculatedStats["2b_0_0"]) / 3
    calculatedStats["chance1B_3"] = 1.0 - (calculatedStats["1b_2_0"] + calculatedStats["1b_1_0"] + calculatedStats["1b_0_0"]) / 3
    calculatedStats["chance3B_2"] = 1.0 - (calculatedStats["3b_2_0"] + calculatedStats["3b_1_0"]) / 2
    calculatedStats["chance2B_2"] = 1.0 - (calculatedStats["2b_2_0"] + calculatedStats["2b_1_0"]) / 2
    calculatedStats["chance1B_2"] = 1.0 - (calculatedStats["1b_2_0"] + calculatedStats["1b_1_0"]) / 2
    calculatedStats["chance3B_1"] = 1.0 - calculatedStats["3b_2_0"]
    calculatedStats["chance2B_1"] = 1.0 - calculatedStats["2b_2_0"]
    calculatedStats["chance1B_1"] = 1.0 - calculatedStats["1b_2_0"]
    calculatedStats["runsHR"] = freq_stats["freqHR"]
    calculatedStats["runs3B_3"] = calculatedStats["chance3B_3"] * freq_stats["freq3B"]
    calculatedStats["runs2B_3"] = calculatedStats["chance2B_3"] * freq_stats["freq2B"]
    calculatedStats["runs1B_3"] = calculatedStats["chance1B_3"] * (freq_stats["freq1B"] + freq_stats["freqBBandHBP"])
    calculatedStats["runs3B_2"] = calculatedStats["chance3B_2"] * freq_stats["freq3B"]
    calculatedStats["runs2B_2"] = calculatedStats["chance2B_2"] * freq_stats["freq2B"]
    calculatedStats["runs1B_2"] = calculatedStats["chance1B_2"] * (freq_stats["freq1B"] + freq_stats["freqBBandHBP"])
    calculatedStats["runs3B_1"] = calculatedStats["chance3B_1"] * freq_stats["freq3B"]
    calculatedStats["runs2B_1"] = calculatedStats["chance2B_1"] * freq_stats["freq2B"]
    calculatedStats["runs1B_1"] = calculatedStats["chance1B_1"] * (freq_stats["freq1B"] + freq_stats["freqBBandHBP"])
    calculatedStats["runsAll"] = (calculatedStats["runsHR"] + calculatedStats["runs3B_3"] + calculatedStats["runs2B_3"] + calculatedStats["runs1B_3"]) * freq_stats["freqPArevised"]
    calculatedStats["valA"] = freq_stats["freqBBandHBP"] + freq_stats["freq1B"] + freq_stats["freq2B"] + freq_stats["freq3B"]
    calculatedStats["valB"] = freq_stats["freq1B"] * 0.8 + freq_stats["freq2B"] * 2 + freq_stats["freq3B"] * 3.2 + freq_stats["freq3B"] * 1.8 + freq_stats["freqBBandHBP"] * 0.1
    calculatedStats["scoreRate"] = calculatedStats["valB"] / (calculatedStats["valB"] + freq_stats["freqOUT"])
    calculatedStats["BSR"] = (calculatedStats["valA"] * calculatedStats["scoreRate"] + freq_stats["freq3B"]) * freq_stats["freqPA"]
    calculatedStats["BJRC"] = freq_stats["freqPA"] * (freq_stats["freq1B"] + 2 * freq_stats["freq2B"] + 3 * freq_stats["freq3B"] + 4 * freq_stats["freq3B"]) * freq_stats["freqPA"]
    return calculatedStats