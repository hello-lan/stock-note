from flask import render_template, current_app, Blueprint, jsonify, flash, request, abort
from flask_login import current_user, login_required

from stocknote.extensions import db
from stocknote.models.note import MyPool, MyInterests
from stocknote.models.stock import Stock
from stocknote.services.quotation import get_latest_price


individual_bp = Blueprint("individual", __name__)


@individual_bp.route("/home")
def index():
    return render_template("home/individual/_index.html")


@individual_bp.route("/stock-pool")
def stock_pool():
    user_id = current_user.id
    
    q = db.session.query(MyPool.code, MyPool.update_time, MyPool.positive_valuation,
                         MyPool.negative_valuation, MyPool.safe_of_margin, Stock.name) \
        .outerjoin(Stock, MyPool.code==Stock.code)  \
        .filter(MyPool.user_id==user_id).all()
    prices = get_latest_price([item.code for item in q])
    items = []
    for item in q:
        latest_price = prices.get(item.code)
        if isinstance(latest_price,float):
            if latest_price < item.negative_valuation * (1 - item.safe_of_margin):
                status = 1
            elif latest_price > item.negative_valuation:
                status = -1
            else:
                status = 0
            latest_price_ = latest_price
        else:
            status = 0
            latest_price_ = "-"
    
        new_item = {
            "code": item.code,
            "name": item.name,
            "valuate_date": item.update_time.strftime("%Y-%m-%d"),
            "positive_valuation": item.positive_valuation,
            "positive_safe_of_margin": item.positive_valuation * (1 - item.safe_of_margin),
            "negative_valuation": item.negative_valuation,
            "negative_safe_of_margin": item.negative_valuation * (1 - item.safe_of_margin),
            "status": status,
            "latest_price": latest_price_,
        }
        items.append(new_item)
    return render_template("home/individual/parts/_stock_pool.html", items=items)


@individual_bp.route("/stock-pool/op/add-stock", methods=["POST"])
def api_op_add_stock_to_pool():
    user_id = current_user.id
    data = request.get_json()
    if "code" not in data:
        return jsonify(message="未接收到请求参数.")
    
    code = data["code"]
    positive_valuation = data.get("positive_valuation", 0)
    negative_valuation = data.get("negative_valuation", 0)
    safe_of_margin = data.get("safe_of_margin", 0.35)
    
    pool_item = MyPool(code=code,
                    positive_valuation=positive_valuation,
                    negative_valuation=negative_valuation,
                    safe_of_margin=safe_of_margin,
                    user_id=user_id
                    )
    db.session.add(pool_item)
    db.session.commit()
    return jsonify(status=200, message="添加成功")


@individual_bp.route("/stock-pool/op/rm-stock", methods=["DELETE"])
def api_op_rm_stock_from_pool():
    user_id = current_user.id
    data = request.get_json()
    if "code" not in data:
        return jsonify(message="未接收到请求参数.")
    code = data["code"]

    MyPool.query.filter_by(code=code,user_id=user_id).delete(synchronize_session=False)
    db.session.commit()
    return jsonify(status=200, message="移除成功")


@individual_bp.route("/stock-pool/op/update-stock", methods=["PATCH"])
def api_op_update_stock_in_pool():
    user_id = current_user.id
    data = request.get_json()
    if "code" not in data:
        return jsonify(message="未接收到请求参数.")
    code = data["code"]
    info = {}
    if "positive_valuation" in data:
        info["positive_valuation"] = data["positive_valuation"]
    if "negative_valuation" in data:
        info["negative_valuation"] = data["negative_valuation"]
    if "safe_of_margin" in data:
        info["safe_of_margin"] = data["safe_of_margin"]
    item = MyPool.query.filter_by(code=code, user_id=user_id).update(info)
    db.session.commit()
    return jsonify(status=200, message="更新成功")


@individual_bp.route("/stock-pool/data/pool-item", methods=["GET"])
def api_data_get_pool_item():
    user_id = current_user.id
    code = request.args.get("code", type=str)
    item = MyPool.query.filter_by(code=code).first_or_404()
    data = {
        "code": item.code,
        "positive_valuation": item.positive_valuation,
        "negative_valuation": item.negative_valuation,
        "safe_of_margin": item.safe_of_margin,
        "user_id": user_id
    }
    return jsonify(status=200, message="", data=data)

   
@individual_bp.route("/my-interests")
def my_interests():
    user_id = current_user.id
    items = db.session.query(MyInterests.code, Stock.name)  \
            .outerjoin(Stock, Stock.code==MyInterests.code)  \
            .filter(MyInterests.user_id==user_id)  \
            .all()
    return render_template("home/individual/parts/_interests.html", items=items)


@individual_bp.route("/my-interests/op/add-stock", methods=["POST"])
def api_op_add_stock_to_interests():
    user_id = current_user.id
    data = request.get_json()
    if "code" not in data:
        return jsonify(message="未接收到请求参数.")
    
    code = data["code"]
    interest = MyInterests(code=code, user_id=user_id)
    db.session.add(interest)
    db.session.commit()
    return jsonify(status=200, message="添加成功")


@individual_bp.route("/my-interests/op/rm-stock", methods=["DELETE"])
def api_op_rm_stock_from_interests():
    user_id = current_user.id
    data = request.get_json()
    if "code" not in data:
        return jsonify(message="未接收到请求参数.")
    
    code = data["code"]
    MyInterests.query.filter_by(code=code).filter_by(user_id=user_id).delete(synchronize_session=False)
    db.session.commit()
    return jsonify(status=200, message="移除成功")


@individual_bp.route("/shell/crawl")
def api_op_shell_crawl_data():
    code = request.args.get("code", type=str)
    import subprocess
    return_code = subprocess.call("cd scripts && bash load_stockdata.sh %s" % code, shell=True)
    if return_code == 0:
        msg = "succeed in crawling %s" % code
    else:
        msg = "failed to crawl %s" % code
    return jsonify(status=200, returnCode=return_code, message=msg)