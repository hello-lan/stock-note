# -*- coding: utf-8 -*-
from flask import render_template, current_app, Blueprint, jsonify, request


home_bp = Blueprint("home", __name__)


@home_bp.route("/")
def index():
    return render_template("home/index.html")


@home_bp.route("/shell/crawl")
def api_op_shell_crawl_data():
    code = request.args.get("code", type=str)
    import subprocess
    return_code = subprocess.call("cd scripts && bash load_stockdata.sh %s" % code, shell=True)
    if return_code == 0:
        msg = "succeed in crawling %s" % code
    else:
        msg = "failed to crawl %s" % code
    return jsonify(status=200, returnCode=return_code, message=msg)