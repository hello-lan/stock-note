from flask import render_template, current_app, Blueprint, jsonify, flash, request, abort

from collections import deque

valuation_bp = Blueprint("valuation", __name__)


@valuation_bp.route("/pe/index")
def pe_index():
    return render_template("home/valuation/_pe_index.html")


@valuation_bp.route("/dcf/index")
def dcf_index():
    return render_template("home/valuation/_dcf_index.html")


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
    return render_template("home/valuation/parts/_dcf_report.html", params=params, data=data)


@valuation_bp.route("/dcf-plus/index")
def dcf_plus_index():
    return render_template("home/valuation/_dcf_plus_index.html")


@valuation_bp.route("/dcf-plus/report")
def dcf_plus_report():
    ## 参数解析
    r = request.args.get("r", type=float, default=0.1)  # 折现率
    profit_0 = request.args.get("profit", type=int)    # 第0年净利润
    equity = request.args.get("equity", type=int)    # 总股本
    # 净利润增长率
    g_1 = request.args.get("g1", type=float)
    g_2 = request.args.get("g2", type=float)
    g_3 = request.args.get("g3", type=float)
    # 派息比例
    dr_0 = request.args.get("dr0", type=float)
    dr_1 = request.args.get("dr1", type=float)
    dr_2 = request.args.get("dr2", type=float)
    dr_3 = request.args.get("dr3", type=float)
    # 第5年的预估市盈率
    pe_5 = request.args.get("pe", type=float)  

    if not all([r, g_1,g_2, g_3, dr_0, dr_1, dr_2, dr_3, pe_5, equity]):
        abort(400)
    # 净利润增长率, 第0年利润已知，故从计算上设当年的增长率为0
    gs = [0, g_1, g_2, g_3, g_3, g_3]   
    # 根据增长率计算后续每天的净利润
    profits = []    # 归母净利润
    p = profit_0
    for g in gs:
        p *= (1 + g) 
        profits.append(p)
    # 派息比例
    drs = [dr_0, dr_1, dr_2, dr_3, dr_3, dr_3]
    # 派息总额，注意，这边假设报告期内的派息方案在次年年底实施(实际情况是次年的四五月份左右)，即第0年没有现金流
    ds_ = [round(dr * p, 2) for dr, p in zip(drs, profits)]
    ds = [0] + ds_[:-1]
    # 现金折现计算各年公允市值
    cap = pe_5 * profits[-1]    # 第5年的市值
    cap_q = deque([cap])
    pe_q = deque([pe_5])
    price_q = deque([cap/equity])
    for d, profit in zip(reversed(ds[1:]), reversed(profits[:-1])):
        cap = (cap + d) / (1 + r)
        cap_q.appendleft(cap)
        pe_q.appendleft(cap / profit)
        price_q.appendleft(cap / equity)
    # results
    data = {
        "gs": gs,
        "profits":profits,
        "drs": drs,
        "ds": ds,
        "capitalizations": cap_q,
        "pes": pe_q,
        "prices": price_q
    }
    return render_template("home/valuation/parts/_dcf_plus_report.html", data=data, r=r, equity=equity)