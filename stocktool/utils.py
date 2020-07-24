from datetime import datetime

import requests
from parsel import Selector


def get_stock_list():
    """ 获取股票列表
    """
    url = "http://file.tushare.org/tsdata/all.csv"
    resp = requests.get(url)
    resp.encoding="gbk"
    text = resp.text.strip()
    data = []
    for line in text.split("\r\n")[1:]:
        code, name, *_ = line.split(",")
        data.append({"code":code, "name":name})
    return data


class FinanceData:
    """ 股票财务数据
    TODO
    """
    headers = {"User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0"}
    xjll_url = "http://stockdata.stock.hexun.com/2008/xjll.aspx"
    zcfz_url = "http://stockdata.stock.hexun.com/2008/zcfz.aspx"
    lr_url = "http://stockdata.stock.hexun.com/2008/lr.aspx"

    def __init__(self, code):
        self.code = code

    def get_sel(self, url, account_date):
        response = requests.get(url, params={"stockid": self.code, "accountdate": account_date})
        selector = Selector(text=response.text)
        return selector


def get_cashflow(code="002003", account_date="2019.12.31"):
    """ 现金流量
    """
    FORMAT = "%Y.%m.%d"
    if isinstance(account_date, datetime):
        account_date = account_date.strftime(FORMAT)
    headers = {"User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0"}
    url = "http://stockdata.stock.hexun.com/2008/xjll.aspx?stockid={code}&accountdate={accountdate}".format(code=code, accountdate=account_date)
    response = requests.get(url, headers=headers)
    # 提取经现金流量净额
    sel = Selector(text=response.text)
    item = {"code": code, "account_date": datetime.strptime(account_date, FORMAT).date()}
    item["net_operating_cashflow"] = sel.xpath("//div[@class='tishi']/strong[contains(text(),'经营活动产生的现金流量净额')]/../../following-sibling::td/div/text()").get("").replace(",","") 
    item["net_investing_cashflow"] = sel.xpath("//div[@class='tishi']/strong[contains(text(),'投资活动产生的现金流量净额')]/../../following-sibling::td/div/text()").get("").replace(",","")
    item["net_financing_cashflow"] = sel.xpath("//div[@class='tishi']/strong[contains(text(),'筹资活动产生的现金流量净额')]/../../following-sibling::td/div/text()").get("").replace(",","") 

    return item