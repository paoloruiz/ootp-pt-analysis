from output_utils.progress.progress_bar import ProgressBar

def calculate_defense(cards):
    progress_bar = ProgressBar(len(cards), "Calculating defensive formulas")
    for card in cards:
        # Catcher
        card["cDefense"] = round(max(card["cx"], (((card["cabi"] * 2 - 125) / 25 * 19.5) + 133) / 2))
        # 1B
        range_factor_1b = 30 + (card["ifrng"] * 2 - 90) * 2 / 25 if card["ifrng"] > 45 else card["ifrng"] * 2 / 3
        err_factor_1b = 18 + (card["iferr"] * 2 - 90) / 25 if card["iferr"] > 45 else card["iferr"] * 2 / 5
        card["1bDefense"] = round(max(card["1bx"], (range_factor_1b + err_factor_1b + card["ifarm"] * 2 / 70 + card["tdp"] * 2 / 70) * (1 + (card["height"] - 155) / 15) / 2))
        # 2B
        card["2bDefense"] = round(max(card["2bx"], ((card["ifrng"] * 2 - 125) / 25 * 21.5 + (card["ifarm"] * 2 - 125) / 25 * 1.5 + (card["tdp"] * 2 - 125) / 25 * 9 + (card["iferr"] * 2 - 125) / 25 * 8.25 + 129) / 2) if card["throws"] == "L" else 0)
        # 3B
        card["3bDefense"] = round(max(card["3bx"], ((card["ifrng"] * 2 - 125) / 25 * 13 + (card["ifarm"] * 2 - 125) / 25 * 17 + (card["tdp"] * 2 - 125) / 25 * 3.25 + (card["iferr"] * 2 - 125) / 25 * 7.5 + 113.5) / 2) if card["throws"] == "L" else 0)
        # SS
        card["ssDefense"] = round(max(card["ssx"], ((card["ifrng"] * 2 - 125) / 25 * 25.5 + (card["ifarm"] * 2 - 125) / 25 * 2 + (card["tdp"] * 2 - 125) / 25 * 8 + (card["iferr"] * 2 - 125) / 25 * 7.5 + 93.75) / 2) if card["throws"] == "L" else 0)
        # LF
        card["lfDefense"] = round(max(card["lfx"], ((card["ofrng"] * 2 - 125) / 25 * 29.5 + (card["ofarm"] * 2 - 125) / 25 * 5.75 + (card["oferr"] * 2 - 125) / 25 * 4 + 149) / 2))
        # CF
        card["cfDefense"] = round(max(card["cfx"], ((card["ofrng"] * 2 - 125) / 25 * 43 + (card["ofarm"] * 2 - 125) / 25 * 1.75 + (card["oferr"] * 2 - 125) / 25 * 3.5 + 78) / 2))
        # RF
        card["rfDefense"] = round(max(card["rfx"], ((card["ofrng"] * 2 - 125) / 25 * 25.5 + (card["ofarm"] * 2 - 125) / 25 * 11 + (card["oferr"] * 2 - 125) / 25 * 4 + 129) / 2))

        progress_bar.increment()
    progress_bar.finish("\n")