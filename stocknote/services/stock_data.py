from stocknote.models.stock import StockGroup, Stock, Indicators, CashFlow, IncomeStatement
from stocknote.extensions import db


def get_stock_indicators(code):
    indicators = Indicators.query \
                .filter_by(code=code) \
                .order_by(Indicators.account_date) \
                .all()
    return indicators


def get_cashflow_revenue_ratios(code):
    """ 自由现金流/销售收入
    """
    q = db.session.query(CashFlow.net_operating_cashflow, CashFlow.account_date, IncomeStatement.revenue) \
        .filter(CashFlow.code==code, CashFlow.code==IncomeStatement.code)  \
        .filter(CashFlow.account_date==IncomeStatement.account_date)  \
        .all()

    ratios = dict()
    for item in q:
        ratios[item.account_date] = 100 * item.net_operating_cashflow / item.revenue
    return ratios
