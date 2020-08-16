from flask import render_template, current_app, Blueprint, jsonify, flash, request, abort

valuation_bp = Blueprint("valuation", __name__)


@valuation_bp.route("/dcf/index")
def dcf_index():
    return render_template("valuation/_dcf_index.html")


@valuation_bp.route("/pe/index")
def pe_index():
    return render_template("valuation/_pe_index.html")


@valuation_bp.route("/dcf/report", methods=["GET"])
def dcf_report():
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
    return render_template("valuation/parts/_dcf_report.html", params=params, data=data)
