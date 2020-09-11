from stocknote.models.stock import StockGroup, Stock, StockIndicators, StockCashFlow, StockIncomeStatement, StockBalanceSheet
from stocknote.extensions import db


def get_stock_indicators(code):
    indicators = StockIndicators.query \
                .filter_by(code=code) \
                .order_by(StockIndicators.account_date) \
                .all()
    return indicators


def get_stock_balance_sheet(code):
    balances = StockBalanceSheet.query  \
               .filter_by(code=code)  \
               .order_by(StockBalanceSheet.account_date)  \
               .all()
    return balances 


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

