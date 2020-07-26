from flask import render_template, current_app, Blueprint, jsonify, flash, request, abort

from stocktool.models import StockGroup, Stock, CashFlow
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


@stock_bp.route("/income", methods=["GET"])
def api_income():
    income = {
        "xLabels": ['2014年报', '2015年报', '2016年报', '2017年报', '2018年报', '2019年报'],
        "name": "营业收入",
        "values": [2.6, 5.9, 9.0, 26.4, 28.7, 70.7]
    }
    return jsonify(income)


@stock_bp.route("/oprating-profit", methods=["GET"])
def api_operating_profit():
    income = {
        "xLabels": ['2001月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'],
        "name": "营业利润",
        "values": [2.6, 5.9, 9.0, 26.4, 28.7, 70.7, 175.6, 182.2, 48.7, 18.8, 6.0, 2.3]
    }
    return jsonify(income)


@stock_bp.route("/net-profit", methods=["GET"])
def api_net_profit():
    income = {
        "xLabels": ['2001月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'],
        "name": "净利润",
        "values": [6.6, 5.9, 9.0, 26.4, 28.7, 70.7, 175.6, 182.2, 148.7, 118.8, 16.0, 22.3]
    }
    return jsonify(income)
    
@stock_bp.route("/profitablity", methods=["GET"])
def api_profitablity():
    data = {
            "xLabels": ['2013', '2014', '2015', '2016', '2017', '2018', '2019'],
            "items": [
                {"name": "自由现金流/销售收入", "values": [0.15, 0.2, 0.18, 0.21, 0.16, 0.15, 0.22]},
                {"name": "净利润率", "values": [0.10, 0.12, 0.125, 0.13, 0.11, 0.121, 0.125]},
                {"name": "净资产收益率(ROE)", "values": [0.09, 0.12, 0.123, 0.13, 0.107, 0.13, 0.125]},
                {"name": "资产收益率(ROA)", "values": [0.05, 0.062, 0.053, 0.061, 0.067, 0.069, 0.065]},
            ]
        }
    return jsonify(data)