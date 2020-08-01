from datetime import datetime, date, timedelta

import requests
from parsel import Selector


class HexunCrawler:
    """ 股票数据爬虫服务
    """
    headers = {"User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0"}
    
    xjll_url = "http://stockdata.stock.hexun.com/2008/xjll.aspx"
    zcfz_url = "http://stockdata.stock.hexun.com/2008/zcfz.aspx"
    lr_url = "http://stockdata.stock.hexun.com/2008/lr.aspx"

    # url = "http://basic.10jqka.com.cn/api/stock/export.php?export=main&type=year&code=600196"

    def _get_selector(self, url, params=None):
        if params is None:
            params = {}
        response = requests.get(url, params=params, headers=self.headers)
        selector = Selector(text=response.text)
        return selector

    def crawl_cashflow(self, code, account_date=None):
        """ 爬取股票code在account_date报告期里的现金流量表相关数据
        Args
        ----
        code : str类型 纯数字的股票代码
        account_date : datetime.date类型, 一年的最后一天的日期

        Returns
        -------
        item : dict类型, 财报中现金流量相关数据
        """
        if account_date is None:
            today = date.today()
            last_year_end = date(today.year, 1, 1) - timedelta(days=1)
            account_date = last_year_end

        url = self.xjll_url

        params={"stockid": code, "accountdate": account_date.strftime("%Y.%m.%d")}
        selector = self._get_selector(url, params)

        item = {"code": code, "account_date": account_date}
        item["net_operating_cashflow"] = selector.xpath("//div[@class='tishi']/strong[contains(text(),'经营活动产生的现金流量净额')]/../../following-sibling::td/div/text()").get("").replace(",","") 
        item["net_investing_cashflow"] = selector.xpath("//div[@class='tishi']/strong[contains(text(),'投资活动产生的现金流量净额')]/../../following-sibling::td/div/text()").get("").replace(",","")
        item["net_financing_cashflow"] = selector.xpath("//div[@class='tishi']/strong[contains(text(),'筹资活动产生的现金流量净额')]/../../following-sibling::td/div/text()").get("").replace(",","") 
        return item

    def crawl_profit(self, code, account_date=None):
        """爬取股票code在account_date报告期里的利润表中的相关数据
        """
        if account_date is None:
            today = date.today()
            last_year_end = date(today.year, 1, 1) - timedelta(days=1)
            account_date = last_year_end

        url = self.lr_url

        params={"stockid": code, "accountdate": account_date.strftime("%Y.%m.%d")}
        selector = self._get_selector(url, params)

        item = {"code": code, "account_date": account_date}
        item["revenue"] = selector.xpath("//div[@class='tishi']/strong[contains(text(),'一、营业收入')]/../../following-sibling::td/div/text()").get("").replace(",","")
        item["oper_cost"] = selector.xpath("//div[@class='tishi']/strong[contains(text(),'营业成本')]/../../following-sibling::td/div/text()").get("").replace(",","")
        item["fin_exp"] = selector.xpath("//div[@class='tishi']/strong[contains(text(),'财务费用')]/../../following-sibling::td/div/text()").get("").replace(",","")
        item["sell_exp"] = selector.xpath("//div[@class='tishi']/strong[contains(text(),'销售费用')]/../../following-sibling::td/div/text()").get("").replace(",","")
        item["admin_exp"] = selector.xpath("//div[@class='tishi']/strong[contains(text(),'管理费用')]/../../following-sibling::td/div/text()").get("").replace(",","")
        item["operate_profit"] = selector.xpath("//div[@class='tishi']/strong[contains(text(),'二、营业利润')]/../../following-sibling::td/div/text()").get("").replace(",","")
        item["total_profit"] = selector.xpath("//div[@class='tishi']/strong[contains(text(),'三、利润总额')]/../../following-sibling::td/div/text()").get("").replace(",","")
        item["net_profit"] = selector.xpath("//div[@class='tishi']/strong[contains(text(),'四、净利润')]/../../following-sibling::td/div/text()").get("").replace(",","")
        return item

    def crawl_balance_sheet(self, code, account_date=None):
        if account_date is None:
            today = date.today()
            last_year_end = date(today.year, 1, 1) - timedelta(days=1)
            account_date = last_year_end

        url = self.zcfz_url

        params={"stockid": code, "accountdate": account_date.strftime("%Y.%m.%d")}
        selector = self._get_selector(url, params)

        item = {"code": code, "account_date": account_date}
        item["net_asset"]
        item["net_profit"] = selector.xpath("//div[@class='tishi']/strong[contains(text(),'所有者权益（或股东权益）合计')]/../../following-sibling::td/div/text()").get("").replace(",","")
        return item