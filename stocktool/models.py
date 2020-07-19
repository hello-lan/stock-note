from stocktool.extensions import db


class Stock(db.Model):
    __tablename__ = "stock"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, index=True, nullable=False)
    name = db.Column(db.String(20), nullable=True)

    def __repr__(self):
        return "%s %s" % (self.code, self.name)


class StockGroup(db.Model):
    __tablename__ = "stock_group"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    stocks = db.relationship("Stock",
                            secondary='stock_group_log',
                            backref=db.backref("groups", lazy="dynamic"),
                            lazy="dynamic")

    def __repr__(self):
        return self.name


StockGroupLog = db.Table("stock_group_log",
    db.Column("stock_code", db.String(20), db.ForeignKey("stock.code")),
    db.Column("group_id", db.Integer, db.ForeignKey("stock_group.id"))
)




