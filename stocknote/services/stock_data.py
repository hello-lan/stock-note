from stocknote.models.stock import StockGroup, Stock, Indicators, CashFlow
from stocknote.extensions import db



def get_stock_indicators(code):
    indicators = Indicators.query \
                .filter_by(code=code) \
                .order_by(Indicators.account_date) \
                .all()
    return indicators