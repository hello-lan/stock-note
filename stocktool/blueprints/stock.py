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

    cashflows = CashFlow.query.filter_by(code=code).all()
    cashflows.sort(key=lambda cf: cf.account_date, reverse=True)

    return render_template("_stock.html", stock=stock, cashflows=cashflows)