# -*- coding: utf-8 -*-
import requests


def crawl_stock_list():
    """ 获取股票列表
    """
    url = "http://file.tushare.org/tsdata/all.csv"
    resp = requests.get(url)
    resp.encoding="gbk"
    text = resp.text.strip()
    data = []
    for line in text.split("\r\n")[1:]:
        code, name, *_ = line.split(",")
        data.append({"code":code, "name":name})
    return data