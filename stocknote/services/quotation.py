import re

import requests


def get_latest_price(codes):
    new_codes = []
    for code in codes:
        if code.isdecimal():
            if code.startswith("6"):
                new_code = "sh" + code
            else:
                new_code = "sz" + code
        else:
            new_code = code
        new_codes.append(new_code)

    result = {}
    url = "http://hq.sinajs.cn/list=" + ",".join(new_codes)
    try:
        response = requests.get(url, timeout=1)
        lines = response.text.split("\n")
    except:
        return result
    
    for line in lines:
        try:
            code = re.findall(r"(\d+)=", line)[0]
            price = re.findall(r"=\"(.*)\"", line)[0].split(",")[3]
            result[code] = round(float(price),2)
        except:
            continue
    return result
