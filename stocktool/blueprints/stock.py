from flask import render_template, current_app, Blueprint, jsonify, flash, request, abort

from stocktool.models.stock import StockGroup, Stock, StockIndicators
from stocktool.extensions import db


stock_bp = Blueprint("stock", __name__)


@stock_bp.route("/detail", methods=["GET"])
def stock_detail():
    data = request.args
    if "code" not in data:
        abort(400)

    code = data["code"]
    stock = Stock.query.filter_by(code=code).first_or_404()
    return render_template("_stock.html", stock=stock)


@stock_bp.route("/revenue", methods=["GET"])
def api_revenue():
    code = request.args.get("code")
    indicators = StockIndicators.query \
                .filter_by(code=code) \
                .order_by(StockIndicators.account_date) \
                .all()
    x_labels = []
    values = []
    rates = []   # 同比
    for item in indicators:
        x_labels.append(item.account_date.strftime("%Y年报"))
        values.append(float(item.total_revenue))
        rate = item.operating_income_yoy
        if rate:
            rates.append(float(rate))
        else:
            rates.append(None)
    
    income = {
        "xLabels": x_labels,
        "name": "营业收入",
        "values": values,
        "rates": rates
    }
    return jsonify(income)


@stock_bp.route("/net-profit-nrgal", methods=["GET"])
def api_net_profit_nrgal():
    """扣非净利润
    """
    code = request.args.get("code")
    indicators = StockIndicators.query \
                .filter_by(code=code) \
                .order_by(StockIndicators.account_date) \
                .all()
    x_labels = []
    values = []
    rates = []   # 同比
    for item in indicators:
        x_labels.append(item.account_date.strftime("%Y年报"))
        values.append(float(item.net_profit_after_nrgal_atsolc))
        rate = item.np_atsopc_nrgal_yoy
        if rate:
            rates.append(float(rate))
        else:
            rates.append(None)
    
    income = {
        "xLabels": x_labels,
        "name": "扣非净利润",
        "values": values,
        "rates": rates
    }
    return jsonify(income)


@stock_bp.route("/net-profit", methods=["GET"])
def api_net_profit():
    code = request.args.get("code")
    indicators = StockIndicators.query \
                .filter_by(code=code) \
                .order_by(StockIndicators.account_date) \
                .all()
    x_labels = []
    values = []
    rates = []
    for item in indicators:
        x_labels.append(item.account_date.strftime("%Y年报"))
        values.append(float(item.net_profit_atsopc))
        rate = item.net_profit_atsopc_yoy
        if rate:
            rates.append(float(rate))
        else:
            rates.append(None)
    
    income = {
        "xLabels": x_labels,
        "name": "净利润",
        "values": values,
        "rates": rates
    }
    return jsonify(income)
    
@stock_bp.route("/profitablity", methods=["GET"])
def api_profitablity():
    code = request.args.get("code")
    indicators = StockIndicators.query \
                .filter_by(code=code) \
                .order_by(StockIndicators.account_date) \
                .all()
    x_labels = []
    roe, mll, jll, roa = [], [], [], []
    for item in indicators:
        x_labels.append(item.account_date.strftime("%Y年报"))
        roe.append(float(item.roe))
        roa.append(float(item.net_interest_of_total_assets))
        mll.append(float(item.gross_selling_rate))
        jll.append(float(item.net_selling_rate))

    data = {
            "xLabels": x_labels,
            "items": [
                # {"name": "自由现金流/销售收入", "values": [0.15, 0.2, 0.18, 0.21, 0.16, 0.15, 0.22]},
                {"name": "销售毛利率", "values": mll},
                {"name": "销售净利率", "values": jll},
                {"name": "净资产收益率(ROE)", "values": roe},
                {"name": "总资产报酬率", "values": roa},
            ]
        }
    return jsonify(data)