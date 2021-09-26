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
        self.session.cookies["cookie"] = "device_id=daab6eaa6ebca44b1f6ae893870ad38e; Hm_lvt_1db88642e346389874251b5a1eded6e3=1632667534; s=bo12iielfp; xq_a_token=737318e45e37283c174e6861710dab688eebe737; xqat=737318e45e37283c174e6861710dab688eebe737; xq_r_token=396a59ce874f08fc58c8d546dffacc59ee1b372b; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTYzNDU3ODI5NCwiY3RtIjoxNjMyNjY3NDgxODE2LCJjaWQiOiJkOWQwbjRBWnVwIn0.QWRmDlszlvKdasmCc_hu-kgUO6dzKLtTkF6_axPbLRbiyHgGYG4PVxJhmozjYYdnVPtLam-58lpiCa02tiGqlxbYxNOFpwkKp4ERBmbOWfFTYR3ZrEOxPs9uiD5YeUnsgeR8FSFgQKkAEHymhG6VAJOHut27mrS2lIBkxzrUGnzASFtTL3GinPt9dJo8QyJGPJtmoQmaLm9qAy9O9x0aDtIiZU87xoUivUbKEaWcCGQhTHRj74mlQQXv-PmivZ28KMJa4jdYhJN00kR1Xb62XxCSW3Y6sayY_N8zW-6dWvhYBk2MUWIS-w4GDJHKfcfPdTSHiPv3lSdgqhkgNPq27Q; u=411632667532575; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1632667553; is_overseas=0"

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
    
