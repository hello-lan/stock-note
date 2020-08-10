from stocknote.models.stock import StockGroup, Stock, StockIndicators, StockCashFlow, StockIncomeStatement
from stocknote.extensions import db


def get_stock_indicators(code):
    indicators = StockIndicators.query \
                .filter_by(code=code) \
                .order_by(StockIndicators.account_date) \
                .all()
    return indicators


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
