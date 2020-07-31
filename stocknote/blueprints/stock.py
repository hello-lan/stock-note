from flask import render_template, current_app, Blueprint, jsonify, flash, request, abort

from stocknote.services.stock_data import get_stock_indicators
from stocknote.models.stock import StockGroup, Stock, StockIndicators, CashFlow as StockCashFlow
from stocknote.extensions import db


stock_bp = Blueprint("stock", __name__)


@stock_bp.route("/detail", methods=["GET"])
def stock_detail():
    data = request.args
    if "code" not in data:
        abort(400)

    code = data["code"]
    stock = Stock.query.filter_by(code=code).first_or_404()
    return render_template("_stock.html", stock=stock)


@stock_bp.route("/valuation", methods=["GET"])
def valuation():
    margin_of_safety = request.args.get("mos", default=0.2, type=float)    # 安全边际
    g = request.args.get("g", default=0.03, type=float)    #  永续年金增长率
    discount_rate = request.args.get("discountRate", default=0.09, type=float)   # 折现率
    total_equity = request.args.get("totalEquity", type=int)
    initial_cashflow = request.args.get("initialCashFlow", type=float)
    _cashflow_growths = request.args.get("cashFlowGrowths", type=str)

    if initial_cashflow is None or _cashflow_growths is None:
        abort(400)
    cashflow_growths = [float(r.strip()) for r in _cashflow_growths.split(",")]

    params = {}
    params["g"] = g
    params["discount_rate"] = discount_rate
    params["margin_of_safety"] = margin_of_safety
    params["cashflow_growths"] = cashflow_growths
    params["initial_cashflow"] = initial_cashflow
    params["total_equity"] = total_equity

    data = {}
    cashflows = []
    cf = initial_cashflow
    for gr in cashflow_growths:
        cf *= (1 + gr)
        cashflows.append(int(cf))

    data["cashflows"] = cashflows
    data["present_values"] = [v/pow(1 + discount_rate, i+1) for i, v in enumerate(data["cashflows"])]
    data["pv_total"] = int(sum(data["present_values"]))
    # 永续年金价值
    data["perpetuity_value"] = int(data["cashflows"][-1] * (1 + g) / (discount_rate - g))
    # 永续年金折现价值
    data["present_value_of_perpetuity_value"] = int(data["perpetuity_value"] / pow(1 + discount_rate, len(cashflow_growths)))
    data["final_valuation"] = data["present_value_of_perpetuity_value"] + data["pv_total"]
    return render_template("_valuation.html", params=params, data=data)


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
    indicators = db.session.query(StockIndicators.account_date, StockIndicators.roe, StockIndicators.total_revenue,
                                  StockIndicators.net_interest_of_total_assets, StockIndicators.gross_selling_rate,
                                  StockIndicators.net_selling_rate, StockCashFlow.net_operating_cashflow) \
                .filter(StockIndicators.code==StockCashFlow.code, StockIndicators.account_date==StockCashFlow.account_date)   \
                .filter(StockIndicators.code==code) \
                .order_by(StockIndicators.account_date) \
                .all()
    x_labels = []
    cashflow_revenue, mll, jll, roa, roe = [], [], [], [], []
    for item in indicators:
        x_labels.append(item.account_date.strftime("%Y年报"))
        cashflow_revenue.append(float(item.net_operating_cashflow/item.total_revenue) * 100)
        roe.append(float(item.roe))
        roa.append(float(item.net_interest_of_total_assets))
        mll.append(float(item.gross_selling_rate))
        jll.append(float(item.net_selling_rate))

    data = {
            "xLabels": x_labels,
            "items": [
                {"name": "自由现金流/销售收入", "values": cashflow_revenue},
                {"name": "销售毛利率", "values": mll},
                {"name": "销售净利率", "values": jll},
                {"name": "ROE", "values": roe},
                {"name": "ROA", "values": roa},
            ]
        }
    return jsonify(data)