# -*- coding: utf-8 -*-
import sys
from operator import attrgetter
from datetime import datetime, date
from time import sleep

import click

sys.path.append("..")
from stocknote import create_app
from stocknote.models.stock import db, Stock, StockIndicators


app = create_app()
app.app_context().push()   # 推入上下文


def check_balancesheet(code:str, dt:date):
    from stocknote.models.stock import StockBalanceSheet

    item = StockBalanceSheet.query.filter_by(code=code,account_date=dt).first()
    if item is None:
        return False 
    else:
        return True


def check_cashflow(code:str, dt:date):
    from stocknote.models.stock import StockCashFlow
    item = StockCashFlow.query.filter_by(code=code,account_date=dt).first()
    if item is None:
        return False 
    else:
        return True

def check_indicators(code:str, dt:date):
    from stocknote.models.stock import StockIndicators
    item = StockIndicators.query.filter_by(code=code,account_date=dt).first()
    if item is None:
        return False 
    else:
        return True

def check_income(code:str, dt:date):
    from stocknote.models.stock import StockIncomeStatement
    item = StockIncomeStatement.query.filter_by(code=code,account_date=dt).first()
    if item is None:
        return False 
    else:
        return True



@click.group()
def cli():
    pass


@cli.command()
def init_stock():
    """ 初始化股票列表
    """
    # from crawlers.base import crawl_stock_list
    from crawlers.xueqiu import XueQiuCrawler

    crawler = XueQiuCrawler()

    data = crawler.crawl_stock_list()
    for item in data:
        stock = Stock(**item)
        db.session.add(stock)
    db.session.commit()


@cli.command()
@click.option("-c", "--code", type=click.STRING, help="股票代码")
@click.option("-d","--data", type=click.Choice(["cashflow","indicators","income","balance", "all"]), default='cashflow')
def crawl(code, data):
    from crawlers.xueqiu import XueQiuCrawler

    crawler = XueQiuCrawler()
    crawler_wrapper = CrawlerWrapper(crawler)

    pools = {"cashflow": crawler_wrapper.add_cashflow,
            "indicators": crawler_wrapper.add_indicators,
            "income": crawler_wrapper.add_income,
            "balance": crawler_wrapper.add_balance,
            "all": crawler_wrapper.add_all
            }
    crawl_func = pools[data]
    crawl_func(code)


class CrawlerWrapper:
    def __init__(self, crawler):
        self.crawler = crawler
    
    def add_cashflow(self, code):
        """ 添加单只股票的现金流量数据
        """
        from stocknote.models.stock import StockCashFlow

        if code is None:
            codes = map(attrgetter("code"), Stock.query.all())
        else:
            codes = [code]

        crawler = self.crawler
        for i, code in enumerate(codes):
            sleep(1)
            print(i, code)
            if code.startswith("6"):
                code_ = "SH" + code
            else:
                # 0、3开头
                code_ = "SZ" + code

            data = crawler.crawl_cashflow(code_)
            for item in data["data"]["list"]:
                if check_cashflow(code, date.fromtimestamp(item["report_date"]/1000)):
                    continue

                cashflow = StockCashFlow(
                    code = code,
                    account_date = date.fromtimestamp(item["report_date"]/1000),
                    net_operating_cashflow = item["ncf_from_oa"][0],
                    net_investing_cashflow = item["ncf_from_ia"][0],
                    net_financing_cashflow = item["ncf_from_fa"][0]
                    )
                db.session.add(cashflow)
            db.session.commit()

    def add_indicators(self, code):
        """ 个股的主要财务指标
        """
        from crawlers.xueqiu import XueQiuCrawler

        crawler = self.crawler

        if code is None:
            codes = map(attrgetter("code"), Stock.query.all())
        else:
            codes = [code]

        for i, code in enumerate(codes):
            sleep(1)
            print(i, code)
            if code.startswith("6"):
                code_ = "SH" + code
            else:
                # 0、3开头
                code_ = "SZ" + code

            data = crawler.crawl_indicator(code_)
            # 解析
            for item in data["data"]["list"]:
                if check_indicators(code, date.fromtimestamp(item["report_date"]/1000)):
                    continue

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

    def add_income(self, code):
        """ 利润表
        """
        from stocknote.models.stock import StockIncomeStatement

        crawler = self.crawler

        if code is None:
            codes = map(attrgetter("code"), Stock.query.all())
        else:
            codes = [code]
        
        for i, code in enumerate(codes):
            sleep(1)
            print(i, code)
            if code.startswith("6"):
                code_ = "SH" + code
            else:
                # 0、3开头
                code_ = "SZ" + code
            data = crawler.crawl_income(code_)
            for item in data["data"]["list"]:
                if check_income(code, date.fromtimestamp(item["report_date"]/1000)):
                    continue

                income = StockIncomeStatement(
                    code = code,
                    account_date = date.fromtimestamp(item["report_date"]/1000),
                    total_revenue = item["total_revenue"][0],
                    revenue = item["revenue"][0],
                    operating_costs = item["operating_costs"][0],
                    operating_cost = item["operating_cost"][0],
                    sales_fee = item["sales_fee"][0],
                    manage_fee = item["manage_fee"][0],
                    financing_expenses = item["financing_expenses"][0],
                    finance_cost_interest_fee = item["finance_cost_interest_fee"][0],
                    asset_impairment_loss = item["asset_impairment_loss"][0],
                    credit_impairment_loss = item["credit_impairment_loss"][0],
                    invest_income = item["invest_income"][0],
                    invest_incomes_from_rr = item["invest_incomes_from_rr"][0],
                    rad_cost = item["rad_cost"][0],
                    asset_disposal_income = item["asset_disposal_income"][0],
                    net_profit = item["net_profit"][0],
                    net_profit_atsopc = item["net_profit_atsopc"][0],
                    operating_taxes_and_surcharge = item["operating_taxes_and_surcharge"][0],
                    op = item["op"][0],
                    profit_total_amt = item["profit_total_amt"][0]
                )
                db.session.add(income)
            db.session.commit()

    def add_balance(self, code):
        """ 资产负债表
        """
        from stocknote.models.stock import StockBalanceSheet

        crawler = self.crawler

        if code is None:
            codes = map(attrgetter("code"), Stock.query.all())
        else:
            codes = [code]

        for i, code in enumerate(codes):
            sleep(1)
            print(i, code)
            if code.startswith("6"):
                code_ = "SH" + code
            else:
                # 0、3开头
                code_ = "SZ" + code
            data = crawler.crawl_balance_sheet(code_)
            for item in data["data"]["list"]:
                if check_balancesheet(code, date.fromtimestamp(item["report_date"]/1000)):
                    continue
                balance = StockBalanceSheet(
                    code = code,
                    account_date = date.fromtimestamp(item["report_date"]/1000),
                    fixed_asset = item["fixed_asset"][0],
                    account_receivable = item["account_receivable"][0],
                    bills_receivable = item["bills_receivable"][0],
                    pre_payment = item["pre_payment"][0],
                    inventory = item["inventory"][0],
                    accounts_payable = item["accounts_payable"][0],
                    bill_payable = item["bill_payable"][0],
                    pre_receivable = item["pre_receivable"][0],
                    total_current_assets = item["total_current_assets"][0],
                    total_noncurrent_assets = item["total_noncurrent_assets"][0],
                    total_assets = item["total_assets"][0],
                    total_current_liab = item["total_current_liab"][0],
                    total_noncurrent_liab = item["total_noncurrent_liab"][0],
                    total_liab = item["total_liab"][0],
                    total_quity_atsopc = item["total_quity_atsopc"][0],
                    minority_equity = item["minority_equity"][0],
                    total_holders_equity = item["total_holders_equity"][0],
                    total_liab_and_holders_equity = item["total_liab_and_holders_equity"][0],
                    fixed_asset_sum = item["fixed_asset_sum"][0],
                    construction_in_process = item["construction_in_process"][0],
                    project_goods_and_material = item["project_goods_and_material"][0],
                    goodwill = item["goodwill"][0],
                    currency_funds = item["currency_funds"][0],
                    st_loan = item["st_loan"][0],
                    lt_loan = item["lt_loan"][0],
                    bond_payable = item["bond_payable"][0],
                    tradable_fnncl_assets = item["tradable_fnncl_assets"][0],
                    tradable_fnncl_liab = item["tradable_fnncl_liab"][0],
                    noncurrent_liab_due_in1y = item["noncurrent_liab_due_in1y"][0],
                    payroll_payable = item["payroll_payable"][0],
                    othr_receivables = item["othr_receivables"][0]
                )
                db.session.add(balance)
            db.session.commit()

    def add_all(self, code):
        self.add_balance(code)
        self.add_cashflow(code)
        self.add_income(code)
        self.add_indicators(code)




if __name__ == "__main__":
    cli()
