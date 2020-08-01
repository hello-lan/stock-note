# -*- coding: utf-8 -*-
"""
@create Time:2020-07-27

@author:LHQ

雪球网爬虫
"""
import requests


class XueQiuCrawler:
    def __init__(self):
        self.session = requests.session()
        self.session.cookies["cookie"] = "xq_a_token=69a6c81b73f854a856169c9aab6cd45348ae1299; xqat=69a6c81b73f854a856169c9aab6cd45348ae1299; xq_r_token=08a169936f6c0c1b6ee5078ea407bb28f28efecf; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTU5ODMyMzAwNCwiY3RtIjoxNTk1ODMwODM1NzYxLCJjaWQiOiJkOWQwbjRBWnVwIn0.Qy0sVDo8hls8Ebc7_XVHrj2httpZX1OfONm3auyGQeJbEc8aH7FM7o02UYMlaAaKtCm0LC52GyGC5MFzimvWwrDwvqA5yeiitxGvo15EkVJjsUzNhpLeefPgG-tYxXRTVOfhD_5n0o6cGuzliY4nGe4vd6gKgAJ-sG0ZkdrirGEIZP4QxzLhARQC8jniZw2YmKmDWXcvrjemvmhVvvvhjcQndZGMxXjeUR-tbW23r_CxY_U4492y4rLiMwYS2uO7ODn1Z1PBqszfcFlFHucW-DwmX4oGVNUSaDk73PHr5ee5zodeuOvPipBqDAoSOUhHY_UPvVrqfE8ImDTfV0FDxg; u=141595830872669; Hm_lvt_1db88642e346389874251b5a1eded6e3=1595830874; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1595830874; device_id=5b9148b4a74da599ae183768ed701d3c"
        self.session.headers.update({"User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0"})

    def crawl_indicator(self, code="SH600196", count=5):
        """ 爬取财务指标
        """
        url = "https://stock.xueqiu.com/v5/stock/finance/cn/indicator.json"
        params = {"symbol": code,
                 "type": "Q4",
                 "is_detail": "true",
                 "count": count,
                 "timestamp": ""
        }
        resp = self.session.get(url, params=params)
        data = resp.json()
        return data
