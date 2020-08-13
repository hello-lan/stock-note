from flask import render_template, current_app, Blueprint, jsonify, flash, request, abort

from operator import itemgetter

from stocknote.models.stock import StockGroup, Stock, StockIndicators, StockCashFlow, StockIncomeStatement
from stocknote.models.individual import BasicInfo
from stocknote.extensions import db
from stocknote.services.stock_data import get_stock_indicators, get_cashflow_revenue_ratios


stock_bp = Blueprint("stock", __name__)


BASIC_INFO_FIELDS = ["scope", "structure","industry_chain", "sales_model", "actual_controller","institutional_ownership", "bonus_and_offering"]


@stock_bp.route("/detail", methods=["GET"])
def stock_detail():
    data = request.args
    if "code" not in data:
        abort(400)

    code = data["code"]
    stock = Stock.query.filter_by(code=code).first_or_404()
    return render_template("stock/_stock_index.html", stock=stock)


@stock_bp.route("/<code>/basic-info", methods=["GET"])
def basic_info(code):
    info = BasicInfo.query.filter_by(code=code).first()
    if info is None:
        info = {}
    return render_template("stock/parts/_basic_info_table.html", info=info)


@stock_bp.route("/<code>/basic-info/partial", methods=["GET"])
def get_partial_basic_info(code):
    field_index = request.args.get("field", type=int)
    if field_index is None:
        return jsonify(message="未接收到请求参数.")
    field = BASIC_INFO_FIELDS[field_index]
    info = BasicInfo.query.filter_by(code=code).first()
    desc = getattr(info, field, "")
    return jsonify(message="success", desc=desc)


@stock_bp.route("/<code>/basic-info/edit", methods=["PATCH"])
def edit_basic_info(code):
    data = request.get_json()
    if "field" not in data:
        return jsonify(message="未接收到请求参数.")
    value = data["value"]
    field_index = data["field"]
    field = BASIC_INFO_FIELDS[field_index]
    info = BasicInfo.query.filter_by(code=code).first()
    if info is None:
        info = BasicInfo(code=code)
    setattr(info, field, value)
    db.session.add(info)
    db.session.commit()
    return jsonify(message="%s更新成功" % field)


@stock_bp.route("/<code>/free-cashflow", methods=["GET"])
def free_cashflow(code):
    q = db.session.query(StockCashFlow.net_operating_cashflow, StockCashFlow.account_date, StockIncomeStatement.revenue, StockIncomeStatement.net_profit) \
        .filter(StockCashFlow.code==code, StockCashFlow.code==StockIncomeStatement.code)  \
        .filter(StockCashFlow.account_date==StockIncomeStatement.account_date)  \
        .order_by(StockCashFlow.account_date)  \
        .all()

    data = []
    pre_cf = None
    for item in q:
        new_item = dict()
        new_item["account_date"] = item.account_date
        new_item["cfr_ratio"] = 100 * item.net_operating_cashflow / item.revenue
        new_item["cfnp_ratio"] = 100 * item.net_operating_cashflow / item.net_profit
        new_item["net_operating_cashflow"] = item.net_operating_cashflow
        if pre_cf is None:
            new_item["nocf_yoy"] = None
        else:
            new_item["nocf_yoy"] = 100 * (item.net_operating_cashflow - pre_cf) / pre_cf
        pre_cf = item.net_operating_cashflow
        data.append(new_item)
    data.sort(key=itemgetter("account_date"), reverse=True)
    return render_template("stock/parts/_cashflow_table.html", cashflows=data)


@stock_bp.route("/<code>/income-percentage", methods=["GET"])
def income_percentage(code):
    """百分率利润表
    """
    q = StockIncomeStatement.query.filter_by(code=code).order_by(StockIncomeStatement.account_date.desc())
    data = []
    for item in q:
        revenue = item.revenue
        new_item = dict()
        new_item["account_date"] = item.account_date
        new_item["revenue"] = 100
        new_item["operating_cost"] = 100 * item.operating_cost/revenue
        new_item["gross_rofit_margin"] = 100 - new_item["operating_cost"]
        new_item["manage_fee"] = 100 * item.manage_fee / revenue
        new_item["rad_cost"] = 100 * item.rad_cost / revenue if item.rad_cost is not None else 0
        new_item["sales_fee"] = 100 * item.sales_fee / revenue
        new_item["financing_expenses"] = 100 * item.financing_expenses / revenue if item.financing_expenses is not None else 0
        new_item["op"] = 100 * item.op / revenue
        new_item["others"] = new_item["gross_rofit_margin"] - new_item["manage_fee"] -  new_item["rad_cost"] - new_item["sales_fee"] - new_item["financing_expenses"] - new_item["op"]
        data.append(new_item)
    return render_template("stock/parts/_income_percentage_table.html", data=data)


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
    return render_template("stock/parts/_valuation_table.html", params=params, data=data)


@stock_bp.route("/<code>/financial-indicators", methods=["GET"])
def financial_indicators(code):
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
    return render_template("stock/parts/_indicators_table.html", indicators=simple_indicators)


@stock_bp.route("/<code>/data/revenue", methods=["GET"])
def api_data_revenue(code):
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


@stock_bp.route("/<code>/data/net-profit-nrgal", methods=["GET"])
def api_data_net_profit_nrgal(code):
    """扣非净利润
    """
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


@stock_bp.route("/<code>/data/net-profit", methods=["GET"])
def api_data_net_profit(code):
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


@stock_bp.route("/<code>/data/profitablity", methods=["GET"])
def api_data_profitablity(code):
    indicators = get_stock_indicators(code)
    x_ticks = []
    mll, jll, roa, roe = [], [], [], []
    for item in indicators:
        account_date = item.account_date
        x_ticks.append(account_date.strftime("%Y年报"))
        roe.append(item.roe)
        roa.append(item.net_interest_of_total_assets)
        mll.append(item.gross_selling_rate)
        jll.append(item.net_selling_rate)

    def map_round(data, n=2):
        return list(map(lambda x: round(x, n), data))

    data = {
        "y_label": "比率(%)",
        "x_ticks": x_ticks,
        "values": {
            "销售毛利率": map_round(mll),
            "销售净利率": map_round(jll),
            "ROE": map_round(roe),
            "ROA": map_round(roa)
            }
        }

    return jsonify(code=200, message="success", data=data)
