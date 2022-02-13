from datetime import datetime

from sqlalchemy import UniqueConstraint

from stocknote.extensions import db


class CheckListQuality(db.Model):
    __tablename__ = "checklist_quality"
    __table_args__ = (
        UniqueConstraint("user_id", "code", name="k_uid_code"),
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, default=1)
    code = db.Column(db.String(10), index=True, nullable=False)
    profitability = db.Column(db.Text, default="-", comment="盈利能力情况")
    growth = db.Column(db.Text, default="-", comment="成长性")
    cashflow = db.Column(db.Text, default="-", comment="现金流状况")
    operation_capability = db.Column(db.Text, default="-", comment="运营能力")
    financial_security = db.Column(db.Text, default="-", comment="财务安全情况")
    financial_stability = db.Column(db.Text, default="-", comment="财务数据稳定性")
    dividend = db.Column(db.Text, default="-", comment="分红情况")
    othr_indicators_comparision = db.Column(db.Text, default="-", comment="其他指标对比情况")
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


class CheckListRisk(db.Model):
    __tablename__ = "checklist_risk"
    __table_args__ = (
        UniqueConstraint("user_id", "code", name="k_uid_code"),
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, default=1)
    code = db.Column(db.String(10), index=True, nullable=False)
    revenue_growth = db.Column(db.Text, default="-", comment="企业营业收入增长的原因")
    operations = db.Column(db.Text, default="-", comment="行业、产地或地区经营情况分析")
    fee = db.Column(db.Text, default="-", comment="看公司费用率或费用绝对数有没有变化")
    investment = db.Column(db.Text, default="-", comment="投资状况分析")
    project_changes = db.Column(db.Text, default="-", comment="募集项目变更情况")
    differences_with_actual_funds_use = db.Column(db.Text, default="-", comment="关注计划投资金额与实际投资金额的差异")
    develope_views_compare_to_past = db.Column(db.Text, default="-", comment="董事会历年关于公司的未来发展的描述有何不同")
    develope_views_compare_to_competitors = db.Column(db.Text, default="-", comment="与同行其他竞争者的行业未来发展看法有何不同")
    develope_views_summary = db.Column(db.Text, default="-", comment="总结分析公司的未来发展")
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class CheckListEvaluate(db.Model):
    __tablename__ = "checklist_evaluate"
    __table_args__ = (
        UniqueConstraint("user_id", "code", name="k_uid_code"),
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, default=1)
    code = db.Column(db.String(10), index=True, nullable=False)
    three_premise = db.Column(db.Text, default="-", comment="估值的三大前提：利润是否为真、利润是否可持续、维持当前盈利是否需要大量资本投入")
    trading_plan_steps = db.Column(db.Text, default="-", comment="交易计划--分几层买入")
    trading_plan_max_ratio = db.Column(db.Text, default="-", comment="交易计划--持仓上限")
    # 非周期股部分
    non_cyclical_profit_growth = db.Column(db.Text, default="-", comment="预估的利润增速--非周期股")
    non_cyclical_net_profit_after_nrgal_atsolc = db.Column(db.Text, default="-", comment="预估的全年扣非净利润--非周期股")
    non_cyclical_net_profit_analysis =  db.Column(db.Text, default="-", comment="对净利润做分析--非周期股")
    non_cyclical_revenue = db.Column(db.Text, default="-", comment="估算公司营业收入--非周期股")
    non_cyclical_profit_rate = db.Column(db.Text, default="-", comment="估算公司的利润率--非周期股")
    non_cyclical_net_profit_discount = db.Column(db.Text, default="-", comment="对净利润现金含量低于100%的企业，对净利润予一定的折扣--非周期股")
    non_cyclical_evaluate = db.Column(db.Text, default="-", comment="计算估值--非周期股")
    non_cyclical_buying_point = db.Column(db.Text, default="-", comment="买点--非周期股")
    non_cyclical_buying_point_2 = db.Column(db.Text, default="-", comment="买点--非周期股")
    non_cyclical_selling_point = db.Column(db.Text, default="-", comment="卖点--非周期股")
    # 周期股部分
    cyclical_net_profit = db.Column(db.Text, default="-", comment="统计过去10年的净利润，计算年均净利润--周期股")
    cyclical_net_profit_discount = db.Column(db.Text, default="-", comment="对净利润现金含量低于1oo%的企业，对净利润予一定的折扣--周期股")
    cyclical_evaluate = db.Column(db.Text, default="-", comment="计算估值--周期股")
    cyclical_buying_point = db.Column(db.Text, default="-", comment="买点--周期股")
    cyclical_selling_point = db.Column(db.Text, default="-", comment="卖点--周期股")
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class ChecklistBanlanceSheet(db.Model):
    __tablename__ = "checklist_balancesheet"
    __table_args__ = (
        UniqueConstraint("user_id", "code", name="k_uid_code"),
    ) 

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, default=1)
    code = db.Column(db.String(10), index=True, nullable=False)
    gdzc_zjzc = db.Column(db.Text, default="-", comment="固定资产的折旧政策")
    gdzc_zjzcbh =  db.Column(db.Text, default="-", comment="固定资产的折旧政策是否变化")
    gdzc_ycjz =  db.Column(db.Text, default="-", comment="固定资产是否隐藏价值")
    gdzc_jtjz =  db.Column(db.Text, default="-", comment="固定资产是否大额计提减值")
    zjgc_sm = db.Column(db.Text, default="-", comment="在建工程数目")
    zjgc_jd = db.Column(db.Text, default="-", comment="在建工程进度")
    kfzc = db.Column(db.Text, default="-", comment="开发支出如何")
    swzc = db.Column(db.Text, default="-", comment="是否有生物资产")
    sy = db.Column(db.Text, default="-", comment="是否有较大的商誉")
    cqdtfy = db.Column(db.Text, default="-", comment="是否有较大的长期待摊费用")
    cydszc = db.Column(db.Text, default="-", comment="是否有持有待售资产")
    hbzj_dqfz = db.Column(db.Text, default="-", comment="货币资金余额是否比短期负债小很多")
    hbzj_yxfz = db.Column(db.Text, default="-", comment="是否货币资金充裕，却借了很多有息或高息负债")
    hbzj_dqyqt = db.Column(db.Text, default="-", comment="定期存款和其他货币资金数据巨大，却缺乏短期可动用流动资金")
    hbzj_qthbzj = db.Column(db.Text, default="-", comment="其他货币资金数额巨大，缺乏合理解释?")
    hbzj_lx = db.Column(db.Text, default="-", comment="货币资金产生的利息收入，显著低于常见理财或存款利率")
    yspj_ypsp = db.Column(db.Text, default="-", comment="银票与商票的比例")
    yspj_sp = db.Column(db.Text, default="-", comment="以往一直是银票，某年突然出现大量商票?")
    yspj_fjrhy = db.Column(db.Text, default="-", comment="非金融企业，却存在与正常经营规模不匹配的应收票据？")
    yszk_dfzz = db.Column(db.Text, default="-", comment="应收账款增长幅度超过同期收入增长幅度?")
    yszk_ys = db.Column(db.Text, default="-", comment="应收账款占营业收入的比例较大，且很大部分（如超过三成）是一年以上的应收款？")
    yszk_hzjtbl = db.Column(db.Text, default="-", comment="坏账计提比例")
    yszk_jtbzbh = db.Column(db.Text, default="-", comment="以往的计提标准一贯宽松，突然严格？或一贯严格，突然宽松？")
    yszk_fq = db.Column(db.Text, default="-", comment="某些时间很长的应收账款突然付清了？")
    yfzk_zz = db.Column(db.Text, default="-", comment="某预付账款是否大幅度增长？")
    qtysk_sm = db.Column(db.Text, default="-", comment="其他应收款数目是否较大")
    ch_jtdjzbbz = db.Column(db.Text, default="-", comment="关注存货的计提跌价准备的标准")
    ch_zj = db.Column(db.Text, default="-", comment="存货增长大幅超过同期营业成本增长，且期末存货账面价值与当期营业成本之比，显著高于同行业水平？")
    ch_mll = db.Column(db.Text, default="-", comment="存货与毛利率同时增加?")
    tzxfc_jlfs = db.Column(db.Text, default="-", comment="计量方式是以成本模式计量还是以公允价值模式计量？")
    cydqtz = db.Column(db.Text, default="-", comment="关注期间所获利息收入和到期确保收回本金")
    jyxjrzc_sm = db.Column(db.Text, default="-", comment="交易性金融资产数额是否比较大？查看附注了解其明细")
    ysjrzc_sm = db.Column(db.Text, default="-", comment="衍生金融资产数额是否比较大？查看附注了解其明细")
    qitafldjrzc_sm = db.Column(db.Text, default="-", comment="其他非流动资产数额是否比较大？查看附注了解其明细")
    cqgqtz_sm = db.Column(db.Text, default="-", comment="长期股权投资数额是否比较大，资产计价是否合适（高估还是低估）")
    cqgqtz_jz = db.Column(db.Text, default="-", comment="长期股权投资是否大额减值")
    cqgqtz_tykz = db.Column(db.Text, default="-", comment="同一控制下公司之间的收购，按照非同一控制处理，创造利润")
    cqgqtz_zgs2lx = db.Column(db.Text, default="-", comment="在资产边缘小额交易，将子公司变为联营公司，操纵利润表")
    cqgqtz_jrzc2lx = db.Column(db.Text, default="-", comment="在资产边缘小额交易，将金融资产变为联营企业，操纵利润表")
    cqgqtz_jc = db.Column(db.Text, default="-", comment="将一篮子减持拆成两次或两次以上的独立交易")
    yxfz_xj = db.Column(db.Text, default="-", comment="企业的现金及现金等价物能否覆盖有息负债")
    yxfz_zzc = db.Column(db.Text, default="-", comment="有息负债占总资产的比例")
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)