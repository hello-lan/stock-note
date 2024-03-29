# -*- coding: utf-8 -*-
from flask import render_template, current_app, Blueprint, jsonify, request
from flask_login import login_required


home_bp = Blueprint("home", __name__)


@home_bp.route("/")
@login_required
def index():
    return render_template("home/index.html")

