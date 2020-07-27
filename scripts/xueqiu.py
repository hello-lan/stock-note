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


if __name__ == "__main__":
    import sys
    from datetime import datetime, date
    from time import sleep

    sys.path.append("..")

    from stocktool import create_app
    from stocktool.models import db, Stock, StockIndicators
    
    app = create_app()
    app.app_context().push()   # 推入上下文


    crawler = XueQiuCrawler()

    for i, stock in enumerate(Stock.query.all()):
        sleep(1)
        code = stock.code
        print(i, code)
        # if i > 10:
        #     break
        if code.startswith("6"):
            code_ = "SH" + code
        else:
            # 0、3开头
            code_ = "SZ" + code

        data = crawler.crawl_indicator(code_)
        # 解析
        for item in data["data"]["list"]:
            indicators = StockIndicators(
                code = code,
                account_date = date.fromtimestamp(item["report_date"]/1000),
                total_revenue = item["total_revenue"][0],
                operating_income_yoy = item["operating_income_yoy"][0],
                net_profit_atsopc = item["net_profit_atsopc"][0],
                net_profit_atsopc_yoy = item["net_profit_atsopc_yoy"][0],
                net_profit_after_nrgal_atsolc = item["net_profit_after_nrgal_atsolc"][0],
                np_atsopc_nrgal_yoy = item["np_atsopc_nrgal_yoy"][0],
                basic_eps = item["basic_eps"][0],
                np_per_share = item["np_per_share"][0],
                capital_reserve = item["capital_reserve"][0],
                undistri_profit_ps = item["undistri_profit_ps"][0],
                operate_cash_flow_ps = item["operate_cash_flow_ps"][0],
                roe = item["avg_roe"][0],     # 字段名不一样
                roe_dlt = item["ore_dlt"][0],   # 字段名不一样
                net_interest_of_total_assets = item["net_interest_of_total_assets"][0],
                rop = item["rop"][0],
                gross_selling_rate = item["gross_selling_rate"][0],
                net_selling_rate = item["net_selling_rate"][0],
                asset_liab_ratio = item["asset_liab_ratio"][0],
                current_ratio = item["current_ratio"][0],
                quick_ratio = item["quick_ratio"][0],
                equity_multiplier = item["equity_multiplier"][0],
                equity_ratio = item["equity_ratio"][0],
                holder_equity = item["holder_equity"][0],
                ncf_from_oa_to_total_liab = item["ncf_from_oa_to_total_liab"][0],
                inventory_turnover_days = item["inventory_turnover_days"][0],
                receivable_turnover_days = item["receivable_turnover_days"][0],
                accounts_payable_turnover_days = item["accounts_payable_turnover_days"][0],
                cash_cycle = item["cash_cycle"][0],
                operating_cycle = item["operating_cycle"][0],
                total_capital_turnover = item["total_capital_turnover"][0],
                inventory_turnover = item["inventory_turnover"][0],
                accounts_receivable_turnover = item["account_receivable_turnover"][0],    # 字段名不一样
                accounts_payable_turnover = item["accounts_payable_turnover"][0],
                current_asset_turnover_rate = item["current_asset_turnover_rate"][0],
                fixed_asset_turnover_ratio = item["fixed_asset_turnover_ratio"][0]
            )
            db.session.add(indicators)
        db.session.commit()