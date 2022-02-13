from datetime import datetime

from sqlalchemy import UniqueConstraint

from stocknote.extensions import db


class MyPool(db.Model):
    __tablename__ = "my_pool"
    __table_args__ = (
        UniqueConstraint("user_id", "code", name="k_uid_code"),
    )
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), index=True, nullable=False)
    positive_valuation = db.Column(db.Float, nullable=False, comment="乐观估值(元/每股)")
    negative_valuation = db.Column(db.Float, nullable=False, comment="保守估值(元/每股)")
    safe_of_margin = db.Column(db.Float, nullable=False, default=0.25, comment="安全边际")
    user_id = db.Column(db.Integer, default=1)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class MyInterests(db.Model):
    __tablename__ = "my_interests"
    __table_args__ = (
        UniqueConstraint("user_id", "code", name="k_uid_code"),
    )

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), index=True, nullable=False)
    user_id = db.Column(db.Integer, default=1)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class BasicInfo(db.Model):
    __tablename__  = "basic_info"
    __table_args__ = (
        UniqueConstraint("user_id", "code", name="k_uid_code"),
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, default=1)
    code = db.Column(db.String(10), index=True, nullable=False)
    scope = db.Column(db.Text, default="-", comment="公司业务范围")
    structure = db.Column(db.Text, default="-", comment="公司业务结构")
    industry_chain = db.Column(db.Text, default="-", comment="上下游情况")
    sales_model = db.Column(db.Text, default="-", comment="销售模式")
    actual_controller = db.Column(db.String, default="-", comment="实际控制人")
    institutional_ownership = db.Column(db.String, default="-", comment="机构持股情况")
    bonus_and_offering = db.Column(db.String, default="-", comment="近几年分红与增发情况")
    competitors = db.Column(db.String, default="-", comment="竞争对手")
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

