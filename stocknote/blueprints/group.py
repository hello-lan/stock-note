from flask import render_template, current_app, Blueprint, jsonify, flash, request

from stocknote.models.stock import StockGroup, Stock
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


@group_bp.route("/<int:group_id>/add-stock", methods=["POST"])
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


@group_bp.route("/<int:group_id>/remove-stock", methods=['DELETE'])
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


    

