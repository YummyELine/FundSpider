#!/usr/bin/env python
# coding:utf-8
import webbrowser

import datetime

import html_downloader
import html_outputer
import html_parser
import time

import send_mail
from Gold.gold_main import GoldMain


class SpiderMain(object):
    def __init__(self):
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.tableFund_fund = TableFund_fund.allAboutFund_fund()
        self.tableFund_hscrapyFund = TableFund_hscrapyfund.hscrapyfund()
        self.get_yesterday_price = get_yesterday_price.getyesterdayprice()

    def craw(self, root_url, fundid, mod):
        if mod == 1:
            new_url = root_url
            # print 'craw{0}'.format(new_url)
            html_cont = self.downloader.download(new_url)
            new_data, his_data = self.parser.parse(html_cont)
            self.tableFund_hscrapyFund.inserthscrapy(his_data['netDate'], his_data['netPrice'], his_data['Rate'],
                                                     fundid)
            if new_data['checkTime'] == '--':
                getprice = self.get_yesterday_price.getprice(fundid)
                self.tableFund_fund.updatefund(getprice[0][0], getprice[0][1], getprice[0][2], fundid)
            else:
                self.tableFund_fund.updatefund(new_data['checkTime'], new_data['nowPrice'], new_data['rate'], fundid)






if __name__ == '__main__':
    from SQL import TableFund_fund, TableFund_hscrapyfund, get_yesterday_price
    from FundCal import fund_main

    time1 = datetime.datetime.now()
    runTimes = time.strptime(str(time1), "%Y-%m-%d %H:%M:%S.%f")
    i = 0
    gTime = None
    for runTime in runTimes:
        if i == 3:
            gTime = runTime
        i += 1

    if 8 <= gTime <= 18:
        sobj = TableFund_fund.allAboutFund_fund()
        urls = sobj.selectUrl()
        for url in urls:
            root_url = url[1]
            fundid = url[0]
            # # 网上爬取数据
            obj_spider = SpiderMain()
            obj_spider.craw(root_url, fundid, 1)
            print root_url
            # 基金的计算
            obj_fund = fund_main.FundMain()
            obj_fund.cal_fund(fundid)
        gold_spider = GoldMain()
        gold_spider.craw('http://www.kxt.com/data/etf/gold.html')
        #
        # sendmail = send_mail.sendmail()
        # sendmail.mail('测试','测试')


















# 测试数据
    # root_url = 'http://fund.eastmoney.com/000930.html?spm=search'
    # fundid = 16
    # # 网上爬取数据
    # obj_spider = SpiderMain()
    # obj_spider.craw(root_url, fundid)
    # # 基金的计算
    # obj_fund = fund_main.FundMain()
    # obj_fund.cal_fund(fundid)


    # outputer = html_outputer.HtmlOutputer()
    # outputer.output_html()
    # # webbrowser.open_new('output.html')
