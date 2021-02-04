data_headers = [
    "t_CID",
    "CID",
    "type",
    "position",
    "first_name",
    "last_name",
    "team",
    "year",
    "tier",
    "ovr",
    "orig_ovr",
    "short_title",
    "height",
    "bats",
    "throws",
    "full_title",
    "con",
    "gap",
    "pow",
    "eye",
    "avk",
    "conVL",
    "gapVL",
    "powVL",
    "eyeVL",
    "avkVL",
    "conVR",
    "gapVR",
    "powVR",
    "eyeVR",
    "avkVR",
    "bun",
    "bfh",
    "stu",
    "mov",
    "ctl",
    "stuVL",
    "movVL",
    "ctlVL",
    "stuVR",
    "movVR",
    "ctlVR",
    "gbpct",
    "velo",
    "stam",
    "hold",
    "ifrng",
    "ifarm",
    "tdp",
    "iferr",
    "ofrng",
    "ofarm",
    "oferr",
    "carm",
    "cabi",
    "px",
    "cx",
    "1bx",
    "2bx",
    "3bx",
    "ssx",
    "lfx",
    "cfx",
    "rfx",
    "spe",
    "ste",
    "run"
]
data_freeze_col = "orig_ovr"
data_hidden_columns = []

pitcher_headers = [
    "t_CID",
    "type",
    "position",
    "first_name",
    "last_name",
    "team",
    "year",
    "tier",
    "ovr",
    "bats",
    "throws",
    "stu",
    "mov",
    "ctl",
    "stuVL",
    "movVL",
    "ctlVL",
    "stuVR",
    "movVR",
    "ctlVR",
    "gbpct",
    "velo",
    "stam",
    "hold",
    "px"
]
pitcher_freeze_col = "bats"
pitcher_hidden_columns = [
    ["t_CID", "t_CID"]
]

batter_headers = [
    "t_CID",
    "type",
    "position",
    "first_name",
    "last_name",
    "team",
    "year",
    "tier",
    "ovr",
    "bats",
    "throws",
    "con",
    "gap",
    "pow",
    "eye",
    "avk",
    "conVL",
    "gapVL",
    "powVL",
    "eyeVL",
    "avkVL",
    "conVR",
    "gapVR",
    "powVR",
    "eyeVR",
    "avkVR",
    "bun",
    "bfh",
    "ifrng",
    "ifarm",
    "tdp",
    "iferr",
    "ofrng",
    "ofarm",
    "oferr",
    "carm",
    "cabi",
    "cx",
    "1bx",
    "2bx",
    "3bx",
    "ssx",
    "lfx",
    "cfx",
    "rfx",
    "spe",
    "ste",
    "run"
]
batter_freeze_col = "bats"
batter_hidden_columns = [
    ["t_CID", "t_CID"],
    ["bun", "bfh"]
]