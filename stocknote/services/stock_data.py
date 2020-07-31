from stocknote.models.stock import StockGroup, Stock, StockIndicators, CashFlow as StockCashFlow
from stocknote.extensions import db



def get_stock_indicators(code):
    indicators = StockIndicators.query \
                .filter_by(code=code) \
                .order_by(StockIndicators.account_date) \
                .all()
    return indicators