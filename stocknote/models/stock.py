from stocknote.extensions import db


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


class Indicators(db.Model):
    __tablename__ = "indicators"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), index=True, nullable=False)
    account_date = db.Column(db.Date, nullable=False, index=True, comment="报告期")
    total_revenue = db.Column(db.Float, comment="营业总收入(元)")
    operating_income_yoy = db.Column(db.Float, comment="营业收入同比增长(%)")
    net_profit_atsopc = db.Column(db.Float, comment="净利润(元)")
    net_profit_atsopc_yoy = db.Column(db.Float, comment="净利润同比增长(%)")
    net_profit_after_nrgal_atsolc = db.Column(db.Float, comment="扣非净利润(元)")
    np_atsopc_nrgal_yoy = db.Column(db.Float, comment="扣非净利润同比增长(%)")
    basic_eps = db.Column(db.Float, comment="每股收益(元)")
    np_per_share = db.Column(db.Float, comment="每股净资产(元)")
    capital_reserve = db.Column(db.Float, comment="每股资本公积金(元)")
    undistri_profit_ps = db.Column(db.Float, comment="每股未分配利润(元)")
    operate_cash_flow_ps= db.Column(db.Float, comment="每股经营现金流(元)")
    roe = db.Column(db.Float, comment="净资产收益率ROE(%)")
    roe_dlt = db.Column(db.Float, comment="净资产收益率-摊薄（%）")
    net_interest_of_total_assets = db.Column(db.Float, comment="总资产报酬率ROA(%)")
    rop = db.Column(db.Float, comment="人力投入回报率(%)")
    gross_selling_rate = db.Column(db.Float, comment="销售毛利率(%)")
    net_selling_rate = db.Column(db.Float, comment="销售净利率(%)")
    asset_liab_ratio = db.Column(db.Float, comment="资产负债率(%)")
    current_ratio = db.Column(db.Float, comment="流动比率")
    quick_ratio = db.Column(db.Float, comment="速动比率")
    equity_multiplier = db.Column(db.Float, comment="权益乘数")
    equity_ratio = db.Column(db.Float, comment="产权比率")
    holder_equity = db.Column(db.Float, comment="股东权益比率")
    ncf_from_oa_to_total_liab = db.Column(db.Float, comment="现金流量比率")
    inventory_turnover_days = db.Column(db.Float, comment="存货周转天数")
    receivable_turnover_days = db.Column(db.Float, comment="应收账款周转天数")
    accounts_payable_turnover_days = db.Column(db.Float, comment="应付账款周转天数")
    cash_cycle = db.Column(db.Float, comment="现金循环周期")
    operating_cycle= db.Column(db.Float, comment="营业周期")
    total_capital_turnover = db.Column(db.Float, comment="总资产周转率")
    inventory_turnover= db.Column(db.Float, comment="存货周转率")
    accounts_receivable_turnover = db.Column(db.Float, comment="应收账款周转率")
    accounts_payable_turnover = db.Column(db.Float, comment="应付账款周转率")
    current_asset_turnover_rate = db.Column(db.Float, comment="流动资产周转率")
    fixed_asset_turnover_ratio = db.Column(db.Float, comment="固定资产周转率")


class IncomeStatement(db.Model):
    __tablename__ = "income_statement"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), index=True, nullable=False)
    account_date = db.Column(db.Date, nullable=False, index=True, comment="报告期")
    total_revenue = db.Column(db.Float, comment="营业总收入")
    revenue = db.Column(db.Float, comment="其中:营业收入")
    operating_costs = db.Column(db.Float, comment="营业总成本")
    operating_cost = db.Column(db.Float, comment="其中:营业成本")
    sales_fee = db.Column(db.Float, comment="销售费用")
    manage_fee = db.Column(db.Float, comment="管理费用")
    rad_cost = db.Column(db.Float, comment="研发费用")
    financing_expenses = db.Column(db.Float, comment="财务费用")
    finance_cost_interest_fee = db.Column(db.Float, comment="其中:利息费用")
    asset_impairment_loss = db.Column(db.Float, comment="资产减值损失")
    credit_impairment_loss = db.Column(db.Float, comment="信用减值损失")
    invest_income = db.Column(db.Float, comment="投资收益")
    invest_incomes_from_rr = db.Column(db.Float, comment="其中：对联营企业和合营企业的投资收益")
    asset_disposal_income = db.Column(db.Float, comment="资产处置收益")
    net_profit = db.Column(db.Float, comment="净利润") 
    net_profit_atsopc = db.Column(db.Float, comment="归属于母公司所有者的净利润") 
    operating_taxes_and_surcharge = db.Column(db.Float, comment="营业税金及附加")


class CashFlow(db.Model):
    __tablename__ = "cash_flow"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), index=True, nullable=False)
    net_operating_cashflow = db.Column(db.Float(20, True), comment="经营活动产生的现金流量净额")
    net_investing_cashflow = db.Column(db.Float(20, True), comment="投资活动产生的现金流量净额")
    net_financing_cashflow = db.Column(db.Float(20, True), comment="筹资活动产生的现金流量净额")
    account_date = db.Column(db.Date, nullable=False, index=True, comment="报告期")
    