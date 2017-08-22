#!/usr/bin/env python
# coding:utf-8
from FundCal import cal_fund_fund, cal_buy_lot, cal_sell_lot, content_main


class FundMain(object):
    def __init__(self):
        self.cal_fund_price = cal_fund_fund.CalFundFund()
        self.cal_buy_lot = cal_buy_lot.CalBuyLot()
        self.cal_sell_lot = cal_sell_lot.CalSellLot()
        self.send_mail = content_main.contentMain()

    def cal_fund(self, id):

        # #计算买入的净值
        self.cal_buy_lot.cal_main(id)

        # 计算卖出的净值
        self.cal_sell_lot.cal_main(id)

        # 计算总的份额，以及平均净值
        self.cal_fund_price.cal_lot_price(id)

        # # 符合规则的自动发邮件进行提醒卖出或者买入
        # self.send_mail.main(id)

