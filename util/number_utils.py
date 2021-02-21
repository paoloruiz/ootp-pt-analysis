def add_ip(old_ip, new_ip):
    new_ip_num = int(old_ip) + int(new_ip)
    new_ip_remainder = int((old_ip % 1) * 10) + int((new_ip) % 1 * 10)
    if new_ip_remainder == 4:
        return new_ip_num + 1.1
    elif new_ip_remainder == 3:
        return new_ip_num + 1
    else:
        return new_ip_num + new_ip_remainder / 10

def ip_to_num(ip):
    return int(ip) + (ip % 1 * 10.0) / 3

def int_or_zero(num):
    try:
        return int(num)
    except:
        return 0

def int_or_negative(num):
    try:
        return int(num)
    except:
        return -1

def float_or_zero(num):
    try:
        return float(num)
    except:
        return 0

def min_max(min_num, num, max_num):
    return max(min(num, max_num), min_num)