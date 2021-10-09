from flask import Blueprint, render_template, request, current_app, url_for, redirect
from flask_login import login_user, logout_user, login_required

from stocknote.models.auth import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_name = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(user_name=user_name).first()
        # current_app.logger.info("username : %s" % user_name)
        if user is not None and user.verify_password(password):
            login_user(user)
            next_url = request.args.get('next')
            if next_url is None or not next_url.startswith("/"):
                next_url = url_for('home.index')
            return redirect(next_url)
    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """退出登录
    """
    logout_user()
    return redirect(url_for('auth.login'))
