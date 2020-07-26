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


stock_group_log = db.Table("stock_group_log",
    db.Column("stock_code", db.String(20), db.ForeignKey("stock.code")),
    db.Column("group_id", db.Integer, db.ForeignKey("stock_group.id"))
)


class BriefFinanceSheet(db.Model):
    __tablename__ = "brief_finance_sheet"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), index=True, nullable=False)
    account_date = db.Column(db.Date, nullable=False, index=True, comment="报告期")


class BriefProfitSheet(db.Model):
    __tablename__ = "brief_profit_sheet"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), index=True, nullable=False)
    account_date = db.Column(db.Date, nullable=False, index=True, comment="报告期")
    revenue = db.Column(db.Float, comment="营业收入")
    oper_cost = db.Column(db.Float, comment="营业成本")
    sell_exp = db.Column(db.Float, comment="销售费用")
    admin_exp = db.Column(db.Float, comment="管理费用")
    fin_exp = db.Column(db.Float, comment="财务费用")
    operate_profit = db.Column(db.Float, comment="营业利润")
    total_profit = db.Column(db.Float, comment="利润总额")
    n_income = db.Column(db.Float, comment="净利润(含少数股东损益)")
    n_income_attr_p = db.Column(db.Float, comment="净利润(不含少数股东损益)")


class BriefBalanceSheet(db.Model):
    __tablename__ = "brief_balance_sheet"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), index=True, nullable=False)
    account_date = db.Column(db.Date, nullable=False, index=True, comment="报告期")
    money_cap = db.Column(db.Float(20, True), comment="货币资金")
    trade_asset = db.Column(db.Float(20, True), comment="交易性金融资产")
    notes_receiv = db.Column(db.Float(20, True), comment="应收票据")
    accounts_receiv = db.Column(db.Float(20, True), comment="应收账款")
    other_receiv = db.Column(db.Float(20, True), comment="其他应收款")
    inventories = db.Column(db.Float(20, True), comment="存货")
    lt_eqt_invest = db.Column(db.Float(20, True), comment="长期股权投资")
    fix_assets = db.Column(db.Float(20, True), comment="固定资产")
    cip = db.Column(db.Float(20, True), comment="在建工程")
    intan_assets = db.Column(db.Float(20, True), comment="无形资产")
    goodwill = db.Column(db.Float(20, True), comment="商誉")

    st_borr = db.Column(db.Float(20, True), comment="短期借款")
    lt_borr = db.Column(db.Float(20, True), comment="长期借款")
    notes_payable = db.Column(db.Float(20, True), comment="应付票据")
    accounts_payable = db.Column(db.Float(20, True), comment="应付账款")
    adv_receipts =  db.Column(db.Float(20, True), comment="预收款")



class CashFlow(db.Model):
    __tablename__ = "cash_flow"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), index=True, nullable=False)
    net_operating_cashflow = db.Column(db.Float(20, True), comment="经营活动产生的现金流量净额")
    net_investing_cashflow = db.Column(db.Float(20, True), comment="投资活动产生的现金流量净额")
    net_financing_cashflow = db.Column(db.Float(20, True), comment="筹资活动产生的现金流量净额")
    account_date = db.Column(db.Date, nullable=False, index=True, comment="报告期")