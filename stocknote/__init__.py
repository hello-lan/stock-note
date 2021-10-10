# -*- coding: utf-8 -*-
import os

import click
from flask import Flask, render_template, jsonify, request


from stocknote.blueprints import (home_bp, compare_bp, stock_bp
    ,individual_bp, valuation_bp, checklist_bp, auth_bp)
from stocknote.extensions import db, login_manager
from stocknote.settings import config
from stocknote.utils import function as FC


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv("FLASK_CONFIG", "development")

    app = Flask("stocknote")
    app.config.from_object(config[config_name])

    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    register_errors(app)
    register_jinjia2_filter(app)
    return app


def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)


def register_blueprints(app):
    app.register_blueprint(home_bp)
    app.register_blueprint(compare_bp, url_prefix="/stock-group")
    app.register_blueprint(stock_bp, url_prefix="/stock")
    app.register_blueprint(individual_bp, url_prefix="/individual")
    app.register_blueprint(valuation_bp, url_prefix="/valuation")
    app.register_blueprint(checklist_bp, url_prefix="/check-list")
    app.register_blueprint(auth_bp, url_prefix="/auth")


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
    @click.option('-u', '--user', required=True, type=click.STRING, help="用户名")
    @click.option('-p', '--password', required=True, type=click.STRING, help="密码")
    @click.option('-n', '--nickname', type=click.STRING, help="密码")
    def create_user(user, password, nickname):
        """创建用户
        """
        from stocknote.models.auth import User
        u = User(name=user, password=password, nick_name=nickname)
        db.session.add(u)
        db.session.commit()
        click.echo("successful create user: %s" % user)

    @app.cli.command()
    def test():
        """run the tests."""
        import unittest
        tests = unittest.TestLoader().discover("tests")
        unittest.TextTestRunner(verbosity=2).run(tests)


def register_jinjia2_filter(app):
    """ 自定义jinjia2过滤器
    """
    @app.template_filter("round")
    def round_ignore_none(value, precision=2, filled_value="-"):
        if value is None:
            return filled_value
        else:
            return round(value, precision)

    @app.template_filter("date")
    def date(value,filled_value="-"):
        if hasattr(value,"date"):
            dt = value.date
            if callable(dt):
                return dt()
            else:
                return dt
        else:
            return filled_value

    @app.template_filter("thousands_format")
    def thousands_format(value, to_int=True):
        if isinstance(value, int) or isinstance(value,float):
            return FC.format_thousand_separator(int(value) if to_int else value)
        else:
            return value

    @app.template_filter("simplify_number")
    def simplify_number(value):
        if isinstance(value, int) or isinstance(value,float):
            if abs(value) >= 1e8:
                _value = round(value/1e8, 2)
                unit = "亿"
            elif abs(value) >= 1e4:
                _value = round(value/1e4, 2)
                unit = "万"
            else:
                _value = value
                unit=""
            value = FC.format_thousand_separator(_value) + unit
        return value

    @app.template_filter("fillna")
    def fillna(value, filled_value="-"):
        if value is None:
            return filled_value
        else:
            return value
