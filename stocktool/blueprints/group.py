from flask import render_template, current_app, Blueprint, jsonify, flash, request

from stocktool.models import StockGroup, Stock
from stocktool.extensions import db


group_bp = Blueprint("group", __name__)


@group_bp.route("/index")
def index():
    groups = StockGroup.query.all()
    return render_template("_group_index.html", groups=groups)


@group_bp.route("/<int:group_id>/detail")
def group_detail(group_id):
    group = StockGroup.query.get_or_404(group_id)
    return render_template("_group_detail.html", group=group)


@group_bp.route("/<int:group_id>/add-stock", methods=["POST"])
def add_stock(group_id):
    group = StockGroup.query.get_or_404(group_id)

    try:
        code = request.get_json()["code"]
    except:
        flash("未接收到请求参数")
    else:
        stock = Stock.query.filter_by(code=code).first()
        if stock is None:
            flash("未查询到代码为 %s 的股票，请确认输入的股票代码是否有误或数据库是否缺失该股票的数据！" % code)
        else:
            group.stocks.append(stock)
            db.session.add(group)
            db.session.commit()
    finally:
        return render_template("_group_detail.html", group=group)


@group_bp.route("/<int:group_id>/remove-stock", methods=['DELETE'])
def remove_stock(group_id):
    group = StockGroup.query.get_or_404(group_id)

    try:
        code = request.get_json()["code"]
    except:
        flash("未接收到请求参数")
    else:
        stock = Stock.query.filter_by(code=code).first()
        if stock is None:
            flash("未查询到代码为 %s 的股票，请确认输入的股票代码是否有误或数据库是否缺失该股票的数据！" % code)
        else:
            group.stocks.remove(stock)
            db.session.add(group)
            db.session.commit()
    finally:
        return render_template("_group_detail.html", group=group)


    

