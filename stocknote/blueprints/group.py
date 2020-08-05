from flask import render_template, current_app, Blueprint, jsonify, flash, request

from collections import defaultdict

from stocknote.models.stock import StockGroup, Stock, IncomeStatement, Indicators, CashFlow
from stocknote.extensions import db


group_bp = Blueprint("group", __name__)


@group_bp.route("/index")
def index():
    groups = StockGroup.query.all()
    return render_template("group/_group_index.html", groups=groups)


@group_bp.route("/create-group", methods=["POST"])
def create_group():
    data = request.get_json()
    if "name" not in data:
        return jsonify(message="未接收到请求参数.")

    group_name = data["name"]
    _group = StockGroup.query.filter_by(name=group_name).first()
    if _group is not None:
        return jsonify(message="该group已经存在.")

    group = StockGroup(name=group_name)
    db.session.add(group)
    db.session.commit()
    return jsonify(message="创建成功")


@group_bp.route("/remove-group", methods=["DELETE"])
def remove_group():
    data = request.get_json()
    if "group_id" not in data:
        return jsonify(message="未接收到请求参数.")

    group_id = data["group_id"]
    group = StockGroup.query.get(group_id)
    if group is None:
        return jsonify(message="该group不存在.")
    
    db.session.delete(group)
    db.session.commit()
    return jsonify(message="成功移除'%s'group" % group.name)


@group_bp.route("/<int:group_id>/detail")
def group_detail(group_id):
    group = StockGroup.query.get_or_404(group_id)
    return render_template("group/_group.html", group=group)


@group_bp.route("/<int:group_id>/op/add-stock", methods=["POST"])
def add_stock(group_id):
    group = StockGroup.query.get_or_404(group_id)

    try:
        code = request.get_json()["code"]
    except:
        return jsonify(message="未接收到请求参数.")
    else:
        stock = Stock.query.filter_by(code=code).first()
        if stock is None:
            msg = "未查询到代码为 %s 的股票，请确认输入的股票代码是否有误或数据库是否缺失该股票的数据！" % code
            return jsonify(message=msg)
        else:
            group.stocks.append(stock)
            db.session.commit()
            return jsonify(message="股票添加成功！")


@group_bp.route("/<int:group_id>/op/remove-stock", methods=['DELETE'])
def remove_stock(group_id):
    group = StockGroup.query.get_or_404(group_id)

    try:
        code = request.get_json()["code"]
    except:
        return jsonify(message="未接收到请求参数.")
    else:
        stock = Stock.query.filter_by(code=code).first()
        if stock is None:
            msg = "未查询到代码为 %s 的股票，请确认输入的股票代码是否有误或数据库是否缺失该股票的数据！" % code
            return jsonify(message=msg)
        else:
            group.stocks.remove(stock)
            db.session.commit()
            return jsonify(message="股票移除成功！")


@group_bp.route("/<int:group_id>/api/data/revenues", methods=["GET"])
def api_data_revenues(group_id):
    group = StockGroup.query.get_or_404(group_id)
    stocks = group.stocks
    code_to_name = {stock.code: stock.name for stock in stocks}
    incomes = IncomeStatement.query.filter(IncomeStatement.code.in_(code_to_name.keys())).all()

    dates = list(set([item.account_date for item in incomes]))
    dates.sort()

    d2i = {d:i for i, d in enumerate(dates)}
    values = defaultdict(lambda:[None] * len(dates))

    for item in incomes:
        name = code_to_name[item.code]
        i = d2i[item.account_date]
        values[name][i] = item.revenue 

    data = {
        "y_label": "金额",
        "x_ticks": [d.strftime("%Y") for d in dates],
        "values": values
        }
    return jsonify(code=200, message="success", data=data)


@group_bp.route("/<int:group_id>/api/data/gross-profit-margins", methods=["GET"])
def api_data_gross_profit_margins(group_id):
    group = StockGroup.query.get_or_404(group_id)
    stocks = group.stocks
    code_to_name = {stock.code: stock.name for stock in stocks}

    indicators = Indicators.query.filter(Indicators.code.in_(code_to_name.keys())).all()

    dates = list(set([item.account_date for item in indicators]))
    dates.sort()

    d2i = {d:i for i, d in enumerate(dates)}
    values = defaultdict(lambda:[None] * len(dates))

    for item in indicators:
        name = code_to_name[item.code]
        i = d2i[item.account_date]
        values[name][i] = item.gross_selling_rate

    data = {
        "y_label": "百分比(%)",
        "x_ticks": [d.strftime("%Y") for d in dates],
        "values": values
        }
    return jsonify(code=200, message="success", data=data)


@group_bp.route("/<int:group_id>/api/data/net-profit-margins", methods=["GET"])
def api_data_net_profit_margins(group_id):
    group = StockGroup.query.get_or_404(group_id)
    stocks = group.stocks
    code_to_name = {stock.code: stock.name for stock in stocks}

    indicators = Indicators.query.filter(Indicators.code.in_(code_to_name.keys())).all()

    dates = list(set([item.account_date for item in indicators]))
    dates.sort()

    d2i = {d:i for i, d in enumerate(dates)}
    values = defaultdict(lambda:[None] * len(dates))

    for item in indicators:
        name = code_to_name[item.code]
        i = d2i[item.account_date]
        values[name][i] = item.net_selling_rate

    data = {
        "y_label": "百分比(%)",
        "x_ticks": [d.strftime("%Y") for d in dates],
        "values": values
        }
    return jsonify(code=200, message="success", data=data)


@group_bp.route("/<int:group_id>/api/data/free-cashflow-to-revenue")
def api_data_free_cashflow_to_revenue(group_id):
    group = StockGroup.query.get_or_404(group_id)
    stocks = group.stocks
    code_to_name = {stock.code: stock.name for stock in stocks}

    results = db.session.query((100*CashFlow.net_operating_cashflow/IncomeStatement.revenue).label("fcf2r"),
                                CashFlow.account_date, CashFlow.code) \
            .filter(CashFlow.code.in_(code_to_name.keys()), CashFlow.code==IncomeStatement.code)  \
            .filter(CashFlow.account_date==IncomeStatement.account_date)  \
            .all()
    
    dates = list(set([item.account_date for item in results]))
    dates.sort()

    d2i = {d:i for i, d in enumerate(dates)}
    values = defaultdict(lambda:[None] * len(dates))

    for item in results:
        name = code_to_name[item.code]
        i = d2i[item.account_date]
        values[name][i] = round(item.fcf2r,2)

    data = {
        "y_label": "百分比(%)",
        "x_ticks": [d.strftime("%Y") for d in dates],
        "values": values
        }
    return jsonify(code=200, message="success", data=data)


@group_bp.route("/<int:group_id>/api/data/roe")
def api_data_roe(group_id):
    group = StockGroup.query.get_or_404(group_id)
    stocks = group.stocks
    code_to_name = {stock.code: stock.name for stock in stocks}

    indicators = Indicators.query.filter(Indicators.code.in_(code_to_name.keys())).all()

    dates = list(set([item.account_date for item in indicators]))
    dates.sort()

    d2i = {d:i for i, d in enumerate(dates)}
    values = defaultdict(lambda:[None] * len(dates))

    for item in indicators:
        name = code_to_name[item.code]
        i = d2i[item.account_date]
        values[name][i] = item.roe

    data = {
        "y_label": "百分比(%)",
        "x_ticks": [d.strftime("%Y") for d in dates],
        "values": values
        }
    return jsonify(code=200, message="success", data=data)


@group_bp.route("/<int:group_id>/api/data/roa")
def api_data_roa(group_id):
    group = StockGroup.query.get_or_404(group_id)
    stocks = group.stocks
    code_to_name = {stock.code: stock.name for stock in stocks}

    indicators = Indicators.query.filter(Indicators.code.in_(code_to_name.keys())).all()

    dates = list(set([item.account_date for item in indicators]))
    dates.sort()

    d2i = {d:i for i, d in enumerate(dates)}
    values = defaultdict(lambda:[None] * len(dates))

    for item in indicators:
        name = code_to_name[item.code]
        i = d2i[item.account_date]
        values[name][i] = item.net_interest_of_total_assets

    data = {
        "y_label": "百分比(%)",
        "x_ticks": [d.strftime("%Y") for d in dates],
        "values": values
        }
    return jsonify(code=200, message="success", data=data)