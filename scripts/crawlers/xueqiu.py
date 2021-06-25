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
        self.session.headers.update({"User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0"})
        self.session.cookies["cookie"] = "Hm_lvt_1db88642e346389874251b5a1eded6e3=1624154850; device_id=24700f9f1986800ab4fcc880530dd0ed; s=c818i016hc; xq_a_token=f257b9741beeb7f05f6296e58041e56c810c8ef8; xqat=f257b9741beeb7f05f6296e58041e56c810c8ef8; xq_r_token=2e05f6c50e316248a8a08ab6a47bc781da7fddfb; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTYyNjQwMzgwNSwiY3RtIjoxNjI0MTU0ODQyODI0LCJjaWQiOiJkOWQwbjRBWnVwIn0.dfVOtvpqlCL7EH3SJjDu3xSO_5SmoxLWmzPA7sJ10Z_bochiqY5_9ZYdMFQbAPnZIK9VR27sxplnlpv6e4DEmoIF5ktZp1DZMrA5ZAuArl3iJ6fZkpDjrOxXq781luYToh497MNUVBJIj3-J0g3l92ISgWZ_7H_IbH8hscVEgUezBZkOhfO59YUouIl5q8xkyya24PgofoYfWTtC6mbHlv3QSEOvMRNNLElAuTvu1hRkDhSz6zWYSm_2xLzfCf8K0bm1TlUgle1qnPbDL0o1rgJRes0S0mnL_OQc1w3LaBJ3vE2gIL-I3Ghop2msNjTtikBYA4rBDrdTk0E74010_A; u=821624154847184; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1624545929; is_overseas=0"

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
    
