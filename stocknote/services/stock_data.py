from functools import lru_cache

from stocknote.models.stock import (StockGroup, Stock, StockIndicators, 
    StockCashFlow, StockIncomeStatement, StockBalanceSheet)
from stocknote.extensions import db


@lru_cache(maxsize=5)
def get_stock_indicators(code, limit=None):
    q = StockIndicators.query \
        .filter_by(code=code) \
        .order_by(StockIndicators.account_date.desc())
    if isinstance(limit, int):
        return q.limit(limit).all()
    else:
        return q.all()


@lru_cache(maxsize=5)
def get_stock_balance_sheet(code, limit=None):
    q = StockBalanceSheet.query  \
        .filter_by(code=code)  \
        .order_by(StockBalanceSheet.account_date.desc())
    if isinstance(limit, int):
        return q.limit(limit).all()
    else:
        return q.all()


@lru_cache(maxsize=5)
def get_stock_income_statement(code, limit=None):
    q = StockIncomeStatement.query  \
        .filter_by(code=code)  \
        .order_by(StockIncomeStatement.account_date.desc())
    if isinstance(limit, int):
        return q.limit(limit).all()
    else:
        return q.all()


def get_cashflow_revenue_ratios(code):
    """ 自由现金流/销售收入
    """
    q = db.session.query(StockCashFlow.net_operating_cashflow, StockCashFlow.account_date, StockIncomeStatement.revenue) \
        .filter(StockCashFlow.code==code, StockCashFlow.code==StockIncomeStatement.code)  \
        .filter(StockCashFlow.account_date==StockIncomeStatement.account_date)  \
        .all()

    ratios = dict()
    for item in q:
        ratios[item.account_date] = 100 * item.net_operating_cashflow / item.revenue
    return ratios


def get_account_receivable_ratio(code):
    """应收账款占收入
    """
    ratiors = dict()
    balances = get_stock_balance_sheet(code)
    indicators = get_stock_indicators(code)
    total_revenues = {indicator.account_date: indicator.total_revenue for indicator in indicators}
    for b in balances:
        d = b.account_date
        total_revenue = total_revenues.get(d)
        if total_revenue is None:
            ratiors[d] = None
        else:
            ratiors[d] = b.account_receivable / total_revenue
    return ratiors


def get_productive_assets(code, limit=None):
    """生产资产 = 固定资产 + 在建工程 + 生产物资
    """
    productive_assets = dict()
    for item in get_stock_balance_sheet(code, limit):
        fixed_asset_sum = item.fixed_asset_sum if item.fixed_asset_sum else 0
        construction_in_process = item.construction_in_process if item.construction_in_process else 0
        project_goods_and_material = item.project_goods_and_material if item.project_goods_and_material else 0
        productive_asset = fixed_asset_sum + construction_in_process + project_goods_and_material
        productive_assets[item.account_date] = productive_asset
    return productive_assets



