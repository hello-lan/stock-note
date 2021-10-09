from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
# login_view 用于设置登录页面的端点,当匿名用户尝试访问受保护的页面时，Flask_Login将重定向到登录页面
login_manager.login_view = 'auth.login'