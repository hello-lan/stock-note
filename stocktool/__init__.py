# -*- coding: utf-8 -*-
import os

import click
from flask import Flask, render_template, jsonify, request

from stocktool.blueprints.home import home_bp
from stocktool.blueprints.group import group_bp
from stocktool.blueprints.stock import stock_bp
from stocktool.extensions import db
from stocktool.settings import config


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv("FLASK_CONFIG", "development")

    app = Flask("stocktool")
    app.config.from_object(config[config_name])

    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    register_errors(app)
    return app


def register_extensions(app):
    db.init_app(app)


def register_blueprints(app):
    app.register_blueprint(home_bp)
    app.register_blueprint(group_bp, url_prefix="/stock-group")
    app.register_blueprint(stock_bp, url_prefix="/stock")


def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('_errors.html', code=400, info='Bad Request'), 400

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('_errors.html', code=403, info='Forbidden'), 403

    @app.errorhandler(404)
    def page_not_found(e):
        if request.accept_mimetypes.accept_json and \
                not request.accept_mimetypes.accept_html:
            response = jsonify(code=404, message='The requested URL was not found on the server.')
            response.status_code = 404
            return response
        return render_template('_errors.html', code=404, info='Page Not Found'), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        response = jsonify(code=405, message='The method is not allowed for the requested URL.')
        response.status_code = 405
        return response

    @app.errorhandler(500)
    def internal_server_error(e):
        if request.accept_mimetypes.accept_json and \
                not request.accept_mimetypes.accept_html \
                or request.host.startswith('api'):
            response = jsonify(code=500, message='An internal server error occurred.')
            response.status_code = 500
            return response
        return render_template('_errors.html', code=500, info='Server Error'), 500


def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')

    @app.cli.command()
    def initstock():
        """ 初始化股票列表
        """
        from stocktool.models import Stock
        from stocktool.utils import get_stock_list

        data = get_stock_list()
        for item in data:
            stock = Stock(**item)
            db.session.add(stock)
        db.session.commit()

    @app.cli.command()
    @click.option("--code", type=click.STRING, help="股票代码")
    @click.option("--account-date", type=click.DateTime(formats=["%Y-%m-%d",]), help="会计日期")
    def add_crashflow(code, account_date):
        """ 添加单只股票的现金流量数据
        """
        from stocktool.models import CashFlow
        from stocktool.utils import get_cashflow

        item = get_cashflow(code, account_date)

        cashflow = CashFlow(**item)
        db.session.add(cashflow)
        db.session.commit()
        


