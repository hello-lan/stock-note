from flask import render_template, current_app, Blueprint, jsonify, flash, request, abort

from collections import defaultdict

from stocknote.extensions import db
from stocknote.models.stock import Stock
from stocknote.models.note import CheckListQuality


checklist_bp = Blueprint("check_list", __name__)


@checklist_bp.route("/api/data/quality", methods=["GET"])
def api_data_quality():
    code = request.args.get("code", type=str)
    checklist = CheckListQuality.query.filter_by(code=code).first()
    checklist = {} if checklist is None else checklist
    html = render_template("stock/check_list/quality.html", code=code, checklist=checklist)
    return jsonify({"message": "success",
                    "data": {"html": html}
                })


@checklist_bp.route("/api/data/quality-partial", methods=["GET"])
def api_data_quality_partial():
    code = request.args.get("code", type=str)
    field = request.args.get("field", type=str)
    if field is None:
        return jsonify(message="未接收到请求参数.")
    info = CheckListQuality.query.filter_by(code=code).first()
    desc = getattr(info, field, "")
    return jsonify({"message": "success",
                    "data": {"desc": desc}
                })


@checklist_bp.route("/api/op/edit-quality-partial", methods=["PATCH"])
def api_op_edit_quality_partial():
    data = request.get_json()
    try:
        code = data["code"]
        field = data["field"]
        value = data["value"]
    except:
        return jsonify(message="未接收到完整的请求参数.")
    checklist = CheckListQuality.query.filter_by(code=code).first()
    if checklist is None:
        checklist = CheckListQuality(code=code)
    setattr(checklist, field, value)
    db.session.add(checklist)
    db.session.commit()
    return jsonify({"message": "%s更新成功" % field,
                    "data": {}
                    })            


@checklist_bp.route("/api/data/risk", methods=["GET"])
def api_data_risk():
    code = request.args.get("code", type=str)
    checklist = {}
    html = render_template("stock/check_list/risk.html", code=code, checklist=checklist)
    return jsonify({"message": "success",
                    "data": {"html": html}
                })