from flask import render_template, current_app, Blueprint, jsonify, flash, request, abort
from flask_login import login_required, current_user

from collections import defaultdict

from stocknote.extensions import db
from stocknote.models.stock import Stock
from stocknote.models.note import CheckListQuality, CheckListRisk, CheckListEvaluate


checklist_bp = Blueprint("check_list", __name__)


## 质量检查清单
@checklist_bp.route("/api/data/quality", methods=["GET"])
@login_required
def api_data_quality():
    """ 完整的质量检查清单表格
    """
    user_id = current_user.id
    code = request.args.get("code", type=str)
    checklist = CheckListQuality.query.filter_by(code=code, user_id=user_id).first()
    checklist = {} if checklist is None else checklist
    html = render_template("stock/check_list/quality.html", code=code, checklist=checklist)
    return jsonify({"message": "success",
                    "data": {"html": html}
                })


@checklist_bp.route("/api/data/quality-partial", methods=["GET"])
def api_data_quality_partial():
    """ 获取质量检查清单中指定字段的内容
    """
    user_id = current_user.id
    code = request.args.get("code", type=str)
    field = request.args.get("field", type=str)
    if field is None:
        return jsonify(message="未接收到请求参数.")
    info = CheckListQuality.query.filter_by(code=code, user_id=user_id).first()
    desc = getattr(info, field, "")
    return jsonify({"message": "success",
                    "data": {"desc": desc}
                })


@checklist_bp.route("/api/op/edit-quality-partial", methods=["PATCH"])
def api_op_edit_quality_partial():
    """ 更新编辑质量检查清单中指定字段的内容
    """
    user_id = current_user.id
    data = request.get_json()
    try:
        code = data["code"]
        field = data["field"]
        value = data["value"]
    except:
        return jsonify(message="未接收到完整的请求参数.")
    checklist = CheckListQuality.query.filter_by(code=code, user_id=user_id).first()
    if checklist is None:
        checklist = CheckListQuality(code=code, user_id=user_id)
    setattr(checklist, field, value)
    db.session.add(checklist)
    db.session.commit()
    return jsonify({"message": "%s更新成功" % field,
                    "data": {}
                    })            


## 避雷检查清单
@checklist_bp.route("/api/data/risk", methods=["GET"])
def api_data_risk():
    """ 完整的避雷清单表格
    """
    user_id = current_user.id
    code = request.args.get("code", type=str)
    checklist = CheckListRisk.query.filter_by(code=code, user_id=user_id).first()
    checklist = {} if checklist is None else checklist
    html = render_template("stock/check_list/risk.html", code=code, checklist=checklist)
    return jsonify({"message": "success",
                    "data": {"html": html}
                })


@checklist_bp.route("/api/data/risk-partial", methods=["GET"])
def api_data_risk_partial():
    """ 获取避雷清单中指定字段的内容
    """
    user_id = current_user.id
    code = request.args.get("code", type=str)
    field = request.args.get("field", type=str)
    if field is None:
        return jsonify(message="未接收到请求参数.")
    info = CheckListRisk.query.filter_by(code=code, user_id=user_id).first()
    desc = getattr(info, field, "")
    return jsonify({"message": "success",
                    "data": {"desc": desc}
                })


@checklist_bp.route("/api/op/edit-risk-partial", methods=["PATCH"])
def api_op_edit_risk_partial():
    """ 更新编辑避雷清单中指定字段的内容
    """
    user_id = current_user.id
    data = request.get_json()
    try:
        code = data["code"]
        field = data["field"]
        value = data["value"]
    except:
        return jsonify(message="未接收到完整的请求参数.")
    checklist = CheckListRisk.query.filter_by(code=code,user_id=user_id).first()
    if checklist is None:
        checklist = CheckListRisk(code=code,user_id=user_id)
    setattr(checklist, field, value)
    db.session.add(checklist)
    db.session.commit()
    return jsonify({"message": "%s更新成功" % field,
                    "data": {}
                    }) 


## 估值检查清单          
@checklist_bp.route("/api/data/evaluate", methods=["GET"])
def api_data_evaluate():
    """ 完整的估值清单表格
    """
    user_id = current_user.id
    code = request.args.get("code", type=str)
    checklist = CheckListEvaluate.query.filter_by(code=code, user_id=user_id).first()
    checklist = {} if checklist is None else checklist
    html = render_template("stock/check_list/evaluate.html", code=code, checklist=checklist)
    return jsonify({"message": "success",
                    "data": {"html": html}
                })


@checklist_bp.route("/api/data/evaluate-partial", methods=["GET"])
def api_data_evaluate_partial():
    """ 获取估值清单中指定字段的内容
    """
    user_id = current_user.id
    code = request.args.get("code", type=str)
    field = request.args.get("field", type=str)
    if field is None:
        return jsonify(message="未接收到请求参数.")
    info = CheckListEvaluate.query.filter_by(code=code, user_id=user_id).first()
    desc = getattr(info, field, "")
    return jsonify({"message": "success",
                    "data": {"desc": desc}
                })


@checklist_bp.route("/api/op/edit-evaluate-partial", methods=["PATCH"])
def api_op_edit_evaluate_partial():
    """ 更新编辑估值清单中指定字段的内容
    """
    user_id = current_user.id
    data = request.get_json()
    try:
        code = data["code"]
        field = data["field"]
        value = data["value"]
    except:
        return jsonify(message="未接收到完整的请求参数.")
    checklist = CheckListEvaluate.query.filter_by(code=code, user_id=user_id).first()
    if checklist is None:
        checklist = CheckListEvaluate(code=code, user_id=user_id)
    setattr(checklist, field, value)
    db.session.add(checklist)
    db.session.commit()
    return jsonify({"message": "%s更新成功" % field,
                    "data": {}
                    }) 