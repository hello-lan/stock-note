from flask import (render_template, current_app, Blueprint, jsonify,
                flash, request, abort, redirect, url_for)
from flask_login import login_required, current_user

from operator import itemgetter, attrgetter
from collections import defaultdict

from stocknote.models.stock import (StockGroup, Stock, StockIndicators, StockCashFlow,
        StockIncomeStatement, StockBalanceSheet)
from stocknote.models.personal.note import BasicInfo
from stocknote.extensions import db
from stocknote.services.stock_data import (get_stock_indicators, get_cashflow_revenue_ratios,
        get_account_receivable_ratio, get_stock_balance_sheet, get_productive_assets,
        get_stock_income_statement, get_bills_receivable_ratio)
from stocknote.utils.function import none_to_zeros


stock_bp = Blueprint("stock", __name__)


@stock_bp.route("/<code>", methods=["GET"])
@login_required
def index(code):
    stock = Stock.query.filter_by(code=code).first_or_404()
    return render_template("stock/index.html", stock=stock)


@stock_bp.route("/detail", methods=["GET"])
def stock_detail():
    code = request.args.get("code", type=str)
    url = url_for('stock.index', code=code)
    return redirect(url)


@stock_bp.route("/report", methods=["GET"])
def api_data_report():
    code = request.args.get("code", type=str)
    stock = Stock.query.filter_by(code=code).first_or_404()
    html = render_template("stock/report/report_index.html", stock=stock)
    return jsonify({"message": "successful",
                    "data": {"html": html}
                })

@stock_bp.route("/basic-info", methods=["GET"])
def api_data_basic_info():
    user_id = current_user.id
    code = request.args.get("code", type=str)
    info = BasicInfo.query.filter_by(code=code, user_id=user_id).first()
    if info is None:
        info = {}
    return jsonify({"message": "successful",
                    "data": {"html": render_template("stock/report/tables/_basic_info.html", info=info)}
                })


@stock_bp.route("/basic-info/partial", methods=["GET"])
def api_data_partial_basic_info():
    user_id = current_user.id
    code = request.args.get("code", type=str)

    field = request.args.get("field", type=str)
    if field is None:
        return jsonify(message="未接收到请求参数.")
    info = BasicInfo.query.filter_by(code=code,user_id=user_id).first()
    desc = getattr(info, field, "")
    return jsonify({"message": "success",
                    "data": {"desc": desc}
                })


@stock_bp.route("/basic-info/edit", methods=["PATCH"])
def api_op_edit_basic_info():
    user_id = current_user.id
    data = request.get_json()
    try:
        code = data["code"]
        field = data["field"]
        value = data["value"]
    except:
        return jsonify(message="未接收到完整的请求参数.")
    # fields = [field for field in BasicInfo.__dict__.keys() if not field.startswith("_")]
    info = BasicInfo.query.filter_by(code=code, user_id=user_id).first()
    if info is None:
        info = BasicInfo(code=code, user_id=user_id)
    setattr(info, field, value)
    db.session.add(info)
    db.session.commit()
    return jsonify({"message": "%s更新成功" % field,
                    "data": {}
                    })


@stock_bp.route("/api/data/brief-balance-sheet", methods=["GET"])
def api_data_brief_balance_sheet():
    code = request.args.get("code", type=str)
    items = get_stock_balance_sheet(code, limit=5)
    return jsonify({"message": "successful",
                    "data": {
                       "html": render_template("stock/report/tables/_brief_balance_sheet.html", items=items)
                    }
                })


@stock_bp.route("/api/data/asset-structure")
def api_data_asset_structure():
    """ 资产结构 - 轻重资产
    """
    code = request.args.get("code", type=str)
    limit = request.args.get("limit", 5, type=int)
    productive_assets = get_productive_assets(code, limit=limit)
    balances = get_stock_balance_sheet(code, limit=limit)
    income_statement = get_stock_income_statement(code, limit=limit)

    tmp = defaultdict(dict)
    for item in balances:
        dt = item.account_date
        tmp[dt]["productive_asset_ratio"] = round(productive_assets[dt] / item.total_assets, 2)
    for item in income_statement:
        dt = item.account_date
        prdasset = productive_assets.get(dt)
        if prdasset:
            tmp[dt]["profit_prdasset_ratio"] = round(item.profit_total_amt / productive_assets[dt], 2)
    data = []
    for dt, item in tmp.items():
        item["account_date"] = dt
        data.append(item)
    data.sort(key=itemgetter("account_date"), reverse=True)
    return jsonify({"message": "successful",
                    "data": {"html": render_template("stock/report/tables/_asset_structure.html", items=data)}
                })


@stock_bp.route("/api/data/five-forces", methods=["GET"])
def api_data_five_forces():
    code = request.args.get("code", type=str)
    limit = request.args.get("limit", 5, type=int)

    balances = get_stock_balance_sheet(code, limit=limit)
    income_statement = get_stock_income_statement(code, limit=limit)
    indicators = get_stock_indicators(code, limit=limit)

    revenues = {item.account_date: item.total_revenue for item in income_statement}
    gross_ratios = {item.account_date: item.gross_selling_rate * 0.01 for item in indicators}
    
    items = []
    for bln in balances:
        dt = bln.account_date
        revenue = revenues.get(dt)
        if not revenue:
            continue
        item = dict()
        item["account_date"] = dt
        item["account_receivable_ratio"] = none_to_zeros(bln.account_receivable) / revenue
        item["pre_payment_ratio"] = none_to_zeros(bln.pre_payment) / revenue
        item["accounts_payable_ratio"] = none_to_zeros(bln.accounts_payable) / revenue
        item["pre_receivable_ratio"] = none_to_zeros(bln.pre_receivable) / revenue
        item["gross_selling_ratio"] = gross_ratios.get(dt)
        items.append(item)
    return jsonify({"message": "successful",
                    "data": {"html": render_template("stock/report/tables/_five_forces.html", items=items)}
                })


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
    return render_template("stock/report/tables/_cashflow.html", cashflows=data)


@stock_bp.route("/api/data/roe-analysis", methods=["GET"])
def api_data_roe_analysis():
    code = request.args.get("code", type=str)
    limit = request.args.get("limit", 10, type=int)

    indicators = get_stock_indicators(code, limit=limit)
    items = []
    for indicator in indicators:
        item = dict()
        item["account_date"] = indicator.account_date
        item["net_profit_rate"] = 100 * indicator.net_profit_atsopc / indicator.total_revenue
        item["total_capital_turnover"] = indicator.total_capital_turnover
        item["equity_multiplier"] = indicator.equity_multiplier
        item["roe"] = indicator.roe_dlt
        items.append(item)
    items.sort(key=itemgetter("account_date"), reverse=True)

    return jsonify({"message": "successful",
                    "data": {"html": render_template("stock/report/tables/_roe.html", items=items)}
                })


@stock_bp.route("/api/data/operation-capability", methods=["GET"])
def api_data_operation_capability():
    code = request.args.get("code", type=str)
    limit = request.args.get("limit", 10, type=int)
    indicators = get_stock_indicators(code, limit=limit)

    return jsonify({"message": "successful",
                    "data": {"html": render_template("stock/report/tables/_turnover.html", items=indicators)}
                })    


@stock_bp.route("/api/data/income-percentage", methods=["GET"])
def api_data_income_percentage():
    """百分率利润表
    """
    code = request.args.get("code", type=str)
    limit = request.args.get("limit", 10, type=int)
    q = get_stock_income_statement(code, limit=limit)

    data = []
    for item in q:
        revenue = item.revenue
        operating_cost = item.operating_cost     # 营业成本
        operating_costs = item.operating_costs   # 营业总成本
        rad_cost = item.rad_cost if item.rad_cost is not None else 0

        new_item = dict()
        new_item["account_date"] = item.account_date
        new_item["gross_rofit_margin"] = 100 * (revenue - operating_cost)/revenue
        new_item["manage_fee"] = 100 * item.manage_fee / revenue
        new_item["rad_cost"] = 100 * rad_cost / revenue
        new_item["sales_fee"] = 100 * item.sales_fee / revenue
        new_item["financing_expenses"] = 100 * item.financing_expenses / revenue if item.financing_expenses is not None else 0
        data.append(new_item)
    return jsonify({"message": "successful",
                    "data": {"html": render_template("stock/report/tables/_income_percentage.html", data=data)}
                })


@stock_bp.route("/api/data/financial-health", methods=["GET"])
def api_data_financial_risk():
    code = request.args.get("code", type=str)
    limit = request.args.get("limit", 10, type=int)

    indicators = get_stock_indicators(code)
    account_receivable_ratios = get_account_receivable_ratio(code)
    balances = get_stock_balance_sheet(code)

    goodwill_ratios = dict()
    currency_interest_liab_ratios = dict()
    for bln in balances:
        dt = bln.account_date
        goodwill_ratios[dt] = none_to_zeros(bln.goodwill)/bln.total_holders_equity
        interest_bearing_liab = none_to_zeros(bln.st_loan) + none_to_zeros(bln.lt_loan) + none_to_zeros(bln.bond_payable) \
                            + none_to_zeros(bln.tradable_fnncl_liab) + none_to_zeros(bln.noncurrent_liab_due_in1y)  # 有息负债
        currency_interest_liab_ratios[dt] = bln.currency_funds / interest_bearing_liab if interest_bearing_liab !=0 else float("inf")

    simple_indicators = []
    for item in indicators:
        dt = item.account_date
        new_item = dict()
        new_item["account_date"] = dt 
        new_item["asset_liab_ratio"] = item.asset_liab_ratio   # 资产负债率
        new_item["equity_multiplier"] = item.equity_multiplier    # 权益乘数
        new_item["equity_ratio"] = item.equity_ratio      # 产权比率
        new_item["current_ratio"] = item.current_ratio    # 流动比率
        new_item["quick_ratio"] = item.quick_ratio        # 速动比率
        new_item["account_receivable_ratio"] = account_receivable_ratios.get(dt)  # 应收账款占收入
        new_item["goodwill_ratio"] = goodwill_ratios.get(dt)
        new_item["currency_interest_liab_ratio"] = currency_interest_liab_ratios.get(dt)
        simple_indicators.append(new_item)
    simple_indicators.sort(key=itemgetter("account_date"), reverse=True)
    return jsonify({"message": "successful",
                    "data": {"html": render_template("stock/report/tables/_financial_risk.html", indicators=simple_indicators)}
                })


@stock_bp.route("/api/data/revenue", methods=["GET"])
def api_data_revenue():
    code = request.args.get("code", type=str)
    limit = request.args.get("limit", 10, type=int)

    indicators = get_stock_indicators(code, limit=limit)
    indicators.sort(key=attrgetter("account_date"))
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
    return jsonify({"message": "successful",
                    "data": {"echarts_bar": income}
                })


@stock_bp.route("/api/data/net-profit-nrgal", methods=["GET"])
def api_data_net_profit_nrgal():
    """扣非净利润
    """
    code = request.args.get("code", type=str)
    limit = request.args.get("limit", 10, type=int)

    indicators = get_stock_indicators(code, limit=limit)
    indicators.sort(key=attrgetter("account_date"))
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
    return jsonify({"message": "successful",
                    "data": {"echarts_bar": income}
                })


@stock_bp.route("/api/data/net-profit", methods=["GET"])
def api_data_net_profit():
    code = request.args.get("code", type=str)
    limit = request.args.get("limit", 10, type=int)

    indicators = get_stock_indicators(code, limit=limit)
    indicators.sort(key=attrgetter("account_date"))

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
    return jsonify({"message": "successful",
                    "data": {"echarts_bar": income}
                })


@stock_bp.route("/api/data/profitablity", methods=["GET"])
def api_data_profitablity():
    code = request.args.get("code", type=str)
    limit = request.args.get("limit", 10, type=int)

    indicators = get_stock_indicators(code, limit=limit)
    indicators.sort(key=attrgetter("account_date"))

    x_ticks = []
    mll, jll, roa, roe = [], [], [], []
    for item in indicators:
        account_date = item.account_date
        x_ticks.append(account_date.strftime("%Y年报"))
        roe.append(item.roe_dlt)
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

    return jsonify({"message":"success",
                    "data": {"echarts_lines": data}
                })


@stock_bp.route("/api/data/total-assets", methods=["GET"])
def api_data_total_assets():
    code = request.args.get("code", type=str)
    limit = request.args.get("limit", 10, type=int)

    balances = get_stock_balance_sheet(code, limit=limit)
    balances.sort(key=attrgetter("account_date"))

    x_labels = []
    values = []
    for item in balances:
        x_labels.append(item.account_date.strftime("%Y年报"))
        values.append(float(item.total_assets))

    data = {
        "xLabels": x_labels,
        "name": "总资产",
        "values": values,
    }
    return jsonify({"message": "successful",
                    "data": {"echarts_bar": data}
                })


@stock_bp.route("/api/data/holders_equity", methods=["GET"])
def api_data_total_holders_equity():
    code = request.args.get("code", type=str)
    limit = request.args.get("limit", 10, type=int)

    balances = get_stock_balance_sheet(code, limit=limit)
    balances.sort(key=attrgetter("account_date"))

    x_labels = []
    values = []

    for bln in balances:
        x_labels.append(bln.account_date.strftime("%Y年报"))
        values.append(float(bln.total_holders_equity))        

    holders_equity = {
        "xLabels": x_labels,
        "name": "净资产",
        "values": values,
    }

    return jsonify({"message": "successful",
                    "data": {"echarts_bar": holders_equity}})


## 排雷
@stock_bp.route("/api/data/warning/currency_funds", methods=["GET"])
def api_data_warning_currency_funds():
    """ 货币资金排雷
    """
    code = request.args.get("code", type=str)
    limit = request.args.get("limit", 5, type=int)

    income_statement = get_stock_income_statement(code, limit=limit)
    balances = get_stock_balance_sheet(code, limit=limit)

    revenues = {item.account_date: item.total_revenue for item in income_statement}
    items = []
    for bl in balances:
        item = {}
        item["account_date"] = bl.account_date
        item["currency_funds"] = bl.currency_funds
        item["crcfnd_assets_ratio"] = bl.currency_funds / bl.total_assets
        item["asset_liab_ratio"] = bl.total_liab / bl.total_assets
        item["crcfnd_revenue_ratio"] = bl.currency_funds /  revenues.get(bl.account_date)
        items.append(item)     

    items.sort(key=itemgetter("account_date"), reverse=True)
    return jsonify({"message":"successful",
                    "data": {"html": render_template("stock/report/tables/_warning_currency_funds.html", items=items)}
                    })

@stock_bp.route("/api/data/warning/account_receivable", methods=["GET"])
def api_data_warning_account_receivable():
    """ 应收票据排雷
    """
    code = request.args.get("code", type=str)
    limit = request.args.get("limit", 5, type=int)

    balances = get_stock_balance_sheet(code, limit=limit)
    indicatos = get_stock_indicators(code, limit=limit)
    actdt_to_rcvb_turnover_days = {ind.account_date:ind.receivable_turnover_days for ind in indicatos}

    ac_ratios = get_account_receivable_ratio(code)
    bc_ratios = get_bills_receivable_ratio(code)
    items = []
    for bl in balances:
        item = {}
        act_dt = bl.account_date
        item["account_date"] = act_dt
        item["act_rcvb_ratio"] = ac_ratios.get(act_dt)
        item["bills_rcvb_ratio"] = bc_ratios.get(act_dt)
        item["bills_rcvb"] = bl.bills_receivable
        item["bill_payable"] = bl.bill_payable
        item["act_rcvb_turnover_days"] = actdt_to_rcvb_turnover_days.get(act_dt)
        item["othr_rcvb_ratio"] = bl.othr_receivables / bl.total_assets if isinstance(bl.othr_receivables, float) else None
        items.append(item)
    items.sort(key=itemgetter("account_date"), reverse=True)
    return jsonify({"message": "successful",
                    "data": {"html": render_template("stock/report/tables/_warning_account_receivable.html", items=items)}
                    })


@stock_bp.route("/api/data/warning/other_assets", methods=["GET"])
def api_data_warning_other_assets():
    """排雷--存货、交易性金融资产、固定资产、在建工程
    """
    code = request.args.get("code", type=str)
    limit = request.args.get("limit", 10, type=int)

    balances = get_stock_balance_sheet(code, limit=limit)
    indicatos = get_stock_indicators(code, limit=limit)

    act_dt_to_fixed_asset_trunover_ratio = {ind.account_date:ind.fixed_asset_turnover_ratio for ind in indicatos}
    act_dt_to_inventory_turnover_days = {ind.account_date:ind.inventory_turnover_days for ind in indicatos}

    items = []
    for bl in balances:
        item = {}
        act_dt = bl.account_date
        item["account_date"] = bl.account_date
        item["inventory_ratio"] =  bl.inventory / bl.total_assets if isinstance(bl.inventory, float) else None
        item["construction_in_process_ratio"] = bl.construction_in_process / bl.total_assets if isinstance(bl.construction_in_process, float) else None
        item["tradable_fnncl_assets_ratio"] = bl.tradable_fnncl_assets / bl.total_assets if isinstance(bl.tradable_fnncl_assets, float) else None
        item["fixed_asset_turnover_ratio"] = act_dt_to_fixed_asset_trunover_ratio.get(act_dt)
        item["inventory_turnover_days"] = act_dt_to_inventory_turnover_days.get(act_dt)
        items.append(item)
    items.sort(key=itemgetter("account_date"), reverse=True)
    return jsonify({"message": "successful",
                    "data": {"html": render_template("stock/report/tables/_warning_other_assets.html", items=items)}
                    })
