def parse_player(player_arr):
    # Parse basic info that will help us calculate extra fields like position or card type
    card_title = player_arr[0]
    ovr = player_arr[1]
    year = player_arr[2]
    last_name = player_arr[3]
    first_name = player_arr[4]
    bats = "S"
    if player_arr[5] == 1:
        bats = "R"
    elif player_arr[5] == 2:
        bats = "L"
    throws = "R" if player_arr[6] == 1 else "L"
    # Harder information to parse
    position = _get_player_position(card_title, player_arr[7], player_arr[8])
    c_type = _get_player_type(card_title, position, first_name)
    tier = _get_player_tier(ovr)
    short_title = first_name + " " + last_name + " " + str(ovr) + " (" + c_type + ")"
    
    # Parse players by each index
    return {
        "t_CID": player_arr[74],
        "CID": player_arr[74],
        "type": c_type,
        "position": position,
        "first_name": first_name,
        "last_name": last_name,
        "team": player_arr[75],
        "year": year,
        "tier": tier,
        "ovr": ovr,
        "orig_ovr": ovr,
        "short_title": short_title.strip(),
        "height": _int_or_zero(player_arr[73]),
        "bats": bats,
        "throws": throws,
        "full_title": card_title,
        "con": player_arr[9],
        "gap": player_arr[10],
        "pow": player_arr[11],
        "eye": player_arr[12],
        "avk": player_arr[13],
        "conVL": player_arr[14],
        "gapVL": player_arr[15],
        "powVL": player_arr[16],
        "eyeVL": player_arr[17],
        "avkVL": player_arr[18],
        "conVR": player_arr[19],
        "gapVR": player_arr[20],
        "powVR": player_arr[21],
        "eyeVR": player_arr[22],
        "avkVR": player_arr[23],
        "bun": player_arr[27],
        "bfh": player_arr[28],
        "stu": player_arr[29],
        "mov": player_arr[30],
        "ctl": player_arr[31],
        "stuVL": player_arr[32],
        "movVL": player_arr[33],
        "ctlVL": player_arr[34],
        "stuVR": player_arr[35],
        "movVR": player_arr[36],
        "ctlVR": player_arr[37],
        "gbpct": player_arr[52],
        "velo": player_arr[53],
        "stam": player_arr[50],
        "hold": player_arr[51],
        "ifrng": player_arr[55],
        "ifarm": player_arr[57],
        "tdp": player_arr[58],
        "iferr": player_arr[56],
        "ofrng": player_arr[61],
        "ofarm": player_arr[63],
        "oferr": player_arr[62],
        "carm": player_arr[60],
        "cabi": player_arr[59],
        "px": player_arr[64],
        "cx": player_arr[65],
        "1bx": player_arr[66],
        "2bx": player_arr[67],
        "3bx": player_arr[68],
        "ssx": player_arr[69],
        "lfx": player_arr[70],
        "cfx": player_arr[71],
        "rfx": player_arr[72],
        "spe": player_arr[24],
        "ste": player_arr[25],
        "run": player_arr[26]
    }

def _get_player_position(card_title, pos_num, extra_num):
    if " SP " in card_title:
        return "SP"
    elif " RP " in card_title:
        return "RP"
    elif " CL " in card_title:
        return "CL"
    elif " C " in card_title:
        return "C"
    elif " 1B " in card_title:
        return "1B"
    elif " 2B " in card_title:
        return "2B"
    elif " 3B " in card_title:
        return "3B"
    elif " SS " in card_title:
        return "SS"
    elif " LF " in card_title:
        return "LF"
    elif " CF " in card_title:
        return "CF"
    elif " RF " in card_title:
        return "RF"
    elif " DH " in card_title:
        return "DH"
    
    if pos_num == 1:
        if extra_num == 12:
            return "RP"
        if extra_num == 13:
            return "CL"
        return "SP"
    if pos_num == 2:
        return "C"
    if pos_num == 3:
        return "1B"
    if pos_num == 4:
        return "2B"
    if pos_num == 5:
        return "3B"
    if pos_num == 6:
        return "SS"
    if pos_num == 7:
        return "LF"
    if pos_num == 8:
        return "CF"
    if pos_num == 9:
        return "RF"
    return "DH"

def _get_player_type(card_title, position, first_name):
    # Lots of special logic to get player type
    position_plus_first_name = " " + position + " " + first_name
    try:
        type_index = card_title.index(position_plus_first_name)
    except:
        type_index = card_title.index(" " + position + " ")
    return card_title[0:type_index]

def _get_player_tier(ovr):
    if ovr > 99:
        return "Perfect"
    if ovr > 89:
        return "Diamond"
    if ovr > 79:
        return "Gold"
    if ovr > 69:
        return "Silver"
    if ovr > 59:
        return "Bronze"
    return "Iron"

def _int_or_zero(num):
    try:
        return int(num)
    except:
        return 0