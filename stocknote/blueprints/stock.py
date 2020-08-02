from flask import render_template, current_app, Blueprint, jsonify, flash, request, abort

from operator import itemgetter

from stocknote.models.stock import StockGroup, Stock, Indicators, CashFlow, IncomeStatement
from stocknote.extensions import db
from stocknote.services.stock_data import get_stock_indicators, get_cashflow_revenue_ratios


stock_bp = Blueprint("stock", __name__)


@stock_bp.route("/detail", methods=["GET"])
def stock_detail():
    data = request.args
    if "code" not in data:
        abort(400)

    code = data["code"]
    stock = Stock.query.filter_by(code=code).first_or_404()
    return render_template("stock/_stock_index.html", stock=stock)


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
    return render_template("stock/_valuation.html", params=params, data=data)


@stock_bp.route("/financial-indicators", methods=["GET"])
def financial_indicators():
    code = request.args.get("code")
    indicators = get_stock_indicators(code)
    simple_indicators = []
    for item in indicators:
        new_item = dict()
        new_item["account_date"] = item.account_date 
        new_item["asset_liab_ratio"] = item.asset_liab_ratio   # 资产负债率
        new_item["equity_multiplier"] = item.equity_multiplier    # 权益乘数
        new_item["equity_ratio"] = item.equity_ratio      # 产权比率
        new_item["current_ratio"] = item.current_ratio    # 流动比率
        new_item["quick_ratio"] = item.quick_ratio        # 速动比率
        new_item["number_of_times_interest_earned"] = "数据缺失"     # 已获利息倍数
        simple_indicators.append(new_item)
    simple_indicators.sort(key=itemgetter("account_date"), reverse=True)
    return render_template("stock/_indicators.html", indicators=simple_indicators)


@stock_bp.route("/revenue", methods=["GET"])
def api_revenue():
    code = request.args.get("code")
    indicators = get_stock_indicators(code)
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
    indicators = get_stock_indicators(code)
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
    indicators = get_stock_indicators(code)
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
    cfr_ratios = get_cashflow_revenue_ratios(code)
    indicators = get_stock_indicators(code)
    x_labels = []
    cashflow_revenue, mll, jll, roa, roe = [], [], [], [], []
    for item in indicators:
        account_date = item.account_date
        x_labels.append(account_date.strftime("%Y年报"))
        roe.append(item.roe)
        roa.append(item.net_interest_of_total_assets)
        mll.append(item.gross_selling_rate)
        jll.append(item.net_selling_rate)
        cashflow_revenue.append(cfr_ratios.get(account_date))

    def map_round(data, n=2):
        return list(map(lambda x: round(x, n), data))

    data = {
            "xLabels": x_labels,
            "yName": "比率(%)",
            "items": [
                {"name": "自由现金流/营业收入", "values": map_round(cashflow_revenue)},
                {"name": "销售毛利率", "values": map_round(mll)},
                {"name": "销售净利率", "values": map_round(jll)},
                {"name": "ROE", "values": map_round(roe)},
                {"name": "ROA", "values": map_round(roa)},
            ]
        }
    return jsonify(data)