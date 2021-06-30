from datetime import datetime

from sqlalchemy import UniqueConstraint

from stocknote.extensions import db


class MyPool(db.Model):
    __tablename__ = "my_pool"
    __table_args__ = (
        UniqueConstraint("user_id", "code", name="k_uid_code"),
    )
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, index=True, nullable=False)
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
    code = db.Column(db.String(10), unique=True, index=True, nullable=False)
    user_id = db.Column(db.Integer, default=1)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class BasicInfo(db.Model):
    __tablename__  = "basic_info"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, index=True, nullable=False)
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


class CheckListQuality(db.Model):
    __tablename__ = "checklist_quality"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, index=True, nullable=False)
    profitability = db.Column(db.Text, default="-", comment="盈利能力情况")
    growth = db.Column(db.Text, default="-", comment="成长性")
    cashflow = db.Column(db.Text, default="-", comment="现金流状况")
    operation_capability = db.Column(db.Text, default="-", comment="运营能力")
    financial_security = db.Column(db.Text, default="-", comment="财务安全情况")
    financial_stability = db.Column(db.Text, default="-", comment="财务数据稳定性")
    dividend = db.Column(db.Text, default="-", comment="分红情况")
    othr_indicators_comparison = db.Column(db.Text, default="-", comment="其他指标对比情况")
    customers = db.Column(db.Text, default="-", comment="客户是谁")
    products = db.Column(db.Text, default="-", comment="提供的产品或服务")
    value_proposition = db.Column(db.Text, default="-", comment="公司的价值主张")
    value_chain = db.Column(db.Text, default="-", comment="价值链")
    profit_model = db.Column(db.Text, default="-", comment="盈利模式")
    business_characteristics = db.Column(db.Text, default="-", comment="生意特性")
    free_cashflow = db.Column(db.Text, default="-", comment="公司自由现金流状况")
    market_spaces = db.Column(db.Text, default="-", comment="公司产品或服务的市场空间")
    growth_momentum = db.Column(db.Text, default="-", comment="公司未来的成长动力")
    potters_five_forces = db.Column(db.Text, default="-", comment="波特五力模型")
    moat = db.Column(db.Text, default="-", comment="护城河")
    moat_level = db.Column(db.Text, default="-", comment="是否有宽阔的护城河及程度")
    management_ethics = db.Column(db.Text, default="-", comment="管理层的能力、格局、价值观、魅力等如何")
    major_shareholders = db.Column(db.Text, default="-", comment="主要股东是谁")
    actual_controller = db.Column(db.Text, default="-", comment="实际控制人是谁")
    state_or_private = db.Column(db.Text, default="-", comment="国企还是民企")
    management_shareholding = db.Column(db.Text, default="-", comment="管理层或主要骨干是否有持股")
    equity_pledge = db.Column(db.Text, default="-", comment="股权质押情况")
    institutionalize = db.Column(db.Text, default="-", comment="公司运作制度化还是高度依赖企业家个人")
    corporate_culture = db.Column(db.Text, default="-", comment="公司企业为文化、价值观、管理质量情况")
    interest_orientation = db.Column(db.Text, default="-", comment="短期利益导向还是重视创造长期价值")
    attitude = db.Column(db.Text, default="-", comment="公司对员工、股东、客户等利益相关者的态度")
    weakness = db.Column(db.Text, default="-", comment="公司的劣势与弱点")
    negative_news = db.Column(db.Text, default="-", comment="有哪些负面消息与观点")
    potential_risk = db.Column(db.Text, default="-", comment="肯能存在的风险")
    decline_prossibility = db.Column(db.Text, default="-", comment="未来有什么原因可能导致公司衰落")
    tenacity = db.Column(db.Text, default="-", comment="如果出现最差的情况，公司能否维持生产和发展")
    past_explainable = db.Column(db.Text, default="-", comment="定性分析能否解释过往业绩")
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)