from datetime import datetime

from stocknote.extensions import db


class Pool(db.Model):
    __tablename__ = "pool"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, index=True, nullable=False)
    positive_valuation = db.Column(db.Float, nullable=False, comment="乐观估值(元/每股)")
    negative_valuation = db.Column(db.Float, nullable=False, comment="保守估值(元/每股)")
    safe_of_margin = db.Column(db.Float, nullable=False, default=0.25, comment="安全边际")
    user_id = db.Column(db.Integer, default=1)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)