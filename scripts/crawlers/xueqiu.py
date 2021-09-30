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
        self.init_cookies()

    def init_cookies(self):
        url = 'https://xueqiu.com'
        rsp = self.session.get(url)
        cookies = requests.utils.dict_from_cookiejar(rsp.cookies)
        self.session.cookies.update(cookies)

    def crawl_stock_list(self):
        url = "https://xueqiu.com/service/v5/stock/screener/quote/list"
        size = 100
        params = dict(
            page=1,
            size=size,
            order="desc",
            orderby="percent",
            order_by="percent",
            market="CN",
            type="sh_sz"
        )
        page = 0
        count = page * size + 1
        result = []
        codes = set()
        while page * size < count:
            page += 1
            print(page)
            params["page"] = page
            resp = self.session.get(url, params=params)
            data = resp.json()["data"]
            count = data["count"]
            for item in data["list"]:
                code=item["symbol"][2:]
                if code not in codes:
                # result.append({"code":code, "name":item["name"]})
                    yield {"code":code, "name":item["name"]}
                codes.add(code)
        # return result


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
    
