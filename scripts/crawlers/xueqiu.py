# -*- coding: utf-8 -*-
"""
@create Time:2020-07-27

@author:LHQ

雪球网爬虫
"""
from datetime import datetime, timedelta

import requests


class XueQiuCrawler:
    def __init__(self):
        self.session = requests.session()
        self.session.cookies["cookie"] = "xq_a_token=69a6c81b73f854a856169c9aab6cd45348ae1299; xqat=69a6c81b73f854a856169c9aab6cd45348ae1299; xq_r_token=08a169936f6c0c1b6ee5078ea407bb28f28efecf; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTU5ODMyMzAwNCwiY3RtIjoxNTk1ODMwODM1NzYxLCJjaWQiOiJkOWQwbjRBWnVwIn0.Qy0sVDo8hls8Ebc7_XVHrj2httpZX1OfONm3auyGQeJbEc8aH7FM7o02UYMlaAaKtCm0LC52GyGC5MFzimvWwrDwvqA5yeiitxGvo15EkVJjsUzNhpLeefPgG-tYxXRTVOfhD_5n0o6cGuzliY4nGe4vd6gKgAJ-sG0ZkdrirGEIZP4QxzLhARQC8jniZw2YmKmDWXcvrjemvmhVvvvhjcQndZGMxXjeUR-tbW23r_CxY_U4492y4rLiMwYS2uO7ODn1Z1PBqszfcFlFHucW-DwmX4oGVNUSaDk73PHr5ee5zodeuOvPipBqDAoSOUhHY_UPvVrqfE8ImDTfV0FDxg; u=141595830872669; Hm_lvt_1db88642e346389874251b5a1eded6e3=1595830874; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1595830874; device_id=5b9148b4a74da599ae183768ed701d3c"
        self.session.cookies["cookie"] = "Hm_lvt_1db88642e346389874251b5a1eded6e3=1596978144,1597076123,1597143593,1597227565; device_id=24700f9f1986800ab4fcc880530dd0ed; s=cg11ke2hs9; __utma=1.1382929846.1596793348.1597154492.1597563314.6; __utmz=1.1596793348.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); xq_a_token=ea60fa2d7aa652e163f0a6c6d320f847675b78a4; xqat=ea60fa2d7aa652e163f0a6c6d320f847675b78a4; xq_r_token=0998ba0d47e72331c7b61632b151f0bf1d94d031; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjc4MzU1ODQwMjIsImlzcyI6InVjIiwiZXhwIjoxNjAwMDQ3NjAzLCJjdG0iOjE1OTc0NTU2MDMxODksImNpZCI6ImQ5ZDBuNEFadXAifQ.cYv81HsOPO3oa4dTOsjJTBkQGaUa4yVHD4yhc3qVKqXXkaCd2w2RgSIV89ifS8CEcEFoapA4x1sF_QZjlA-5ZESfGdhOsjEZQjzCFDsH9c7S9uYV6lfOTnY97QhLhzQAXHmS7ZF2GCUUxl2wMmUECU_IvgfrkN3cq60FVyWqfu5-_TYFQRGu2P7uetcSTP8fRx_Fnn1crvWHZ-rHYKf3fbpl_y62BtoTGVWLz1QT6-HtHj08yJtFng1LFq_YquNIjd3RT0LcRsAtamR-fNBzHEVdiSKCdhFYPvmn1u1Q9WgcLEu_ZV0SY7gnl550jvcGFxkbyrVtAyIoZvyGG164BQ; xq_is_login=1; bid=abb400b2f2b2d378264aa4620f456a27_kdmm5mb1; aliyungf_tc=AQAAAAUmch9tygkAIgRXcqs/41xw+psN; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1597982714; __utmc=1; snbim_minify=true; u=121597478629324; cookiesu=121597478629324; acw_tc=2760823a15979825994652732e553909b8017ad6837accbfd4008be9ec9445; is_overseas=0"
        self.session.headers.update({"User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0"})

    def crawl_indicator(self, code="SH600196", count=10):
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

    def crawl_income(self, code="SH600196", count=10):
        """爬取利润表
        """
        url = "https://stock.xueqiu.com/v5/stock/finance/cn/income.json"
        params = {
            "symbol": code,
            "type": "Q4",
            "is_detail": "true",
            "count":count,
            "timestamp":""
        }
        resp = self.session.get(url, params=params)
        data = resp.json()
        return data

    def crawl_cashflow(self, code="SH600196", count=10):
        """爬取现金流量表
        """
        url = "https://stock.xueqiu.com/v5/stock/finance/cn/cash_flow.json"
        params = {
            "symbol": code,
            "type": "Q4",
            "is_detail": "true",
            "count":count,
            "timestamp":""
        }
        resp = self.session.get(url, params=params)
        data = resp.json()
        return data

    def crawl_balance_sheet(self, code, count=10):
        url = "https://stock.xueqiu.com/v5/stock/finance/cn/balance.json"
        params = {
            "symbol": code,
            "type": "Q4",
            "is_detail": "true",
            "count":count,
            "timestamp":""
        }
        resp = self.session.get(url, params=params)
        data = resp.json()
        return data

    def filter_stocks(self, page=1, size=50):
        """雪球选股器
        """
        url = "https://xueqiu.com/service/screener/screen"

        query = {"category":"CN",
                "exchange":"sh_sz",
                "areacode":"",
                "indcode":"",
                "order_by":"symbol",
                "order":"desc",
                "page":str(page),
                "size":str(size),
                "only_count":"0",
                "current":"",
                "pct":"",
                }
        
        now_year = datetime.now().year
        for y in range(now_year-5, now_year):
            key_1 = "roediluted.%d1231" % y
            key_2 = "niota.%d1231" % y
            query[key_1] = "20_1000"
            query[key_2] = "8_1000"

        response = self.session.get(url, params=query)
        return response.json()

    def filter_stocks2(self, page=1, size=50):
        url = "https://xueqiu.com/service/screener/screen"

        query = {"category":"CN",
                "exchange":"sh_sz",
                "areacode":"",
                "indcode":"",
                "order_by":"symbol",
                "order":"desc",
                "page":str(page),
                "size":str(size),
                "only_count":"0",
                "current":"",
                "pct":"",
                "pb":"0_1.5",
                "dy_l":"0.1_17.67",
                "pelyr":"-1394.78_4288.9"}
        response = self.session.get(url, params=query)
        return response.json()      
    