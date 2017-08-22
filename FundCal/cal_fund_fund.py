#!/usr/bin/env python
# coding:utf-8
import sql_class


class CalFundFund(object):
    def __init__(self):
        self.mysql = sql_class.SqlConnect()

    def cal_lot_price(self, id):
        buy_datas =  self.cal_buy(id)
        buy_lot = 0
        buy_money = 0
        buy_factorage = 0
        buy_avtSum = 0
        buy_i =0
        # 买入的份儿相加  买入的份额*当时的净值
        for buy_data in buy_datas:
            buy_i += 1
            buy_lot += buy_data[0]
            price = buy_data[0]*buy_data[1]
            buy_money += price
            if buy_data[2] is not None:
                buy_factorage += buy_data[2]
                buy_avtSum += buy_data[2]/buy_data[0]

        if buy_i == 0:
            buy_avtF = 0
        else:
            buy_avtF = buy_avtSum / buy_i


        sell_datas =  self.cal_sell(id)
        sell_lot = 0
        sell_money = 0
        sell_factorage = 0
        # 卖出的份儿相加  卖出的份额*当时的净值
        for sell_data in sell_datas:
            sell_lot += sell_data[0]
            price = sell_data[0] * sell_data[1]
            if sell_data[3] is not None:
                sell_factorage += sell_data[3]
            # 如果是分红份额就是0
            if sell_data[0] == 0:
                sell_money += sell_data[2]
            sell_money += price
        lot = buy_lot - sell_lot
        if lot == 0:
            netprice = 0
        else:
            netprice = ((buy_money - sell_money + sell_factorage ) / (buy_lot - sell_lot)) +buy_avtF
        totalfactorage = sell_factorage + buy_factorage
        self.update_fund_fund(round(netprice,4),lot ,id, totalfactorage)

    def update_fund_fund(self, netprice, lot, id, totalfactorage):
        cx = self.mysql.conn()
        cx.execute("""update fund_fund set totallot = ? , positionprice = ? ,totalfactorage=?
 where id = ? """, (lot, netprice, totalfactorage, id))
        cx.commit()
        cx.close()

    def cal_buy(self,id):
        lis = []
        cx = self.mysql.conn()
        cur = cx.cursor()
        gcurs = cur.execute("""select lot,netprice, factorage from fund_buyfund 
where fundid_id =? and lot is not NULL  and netprice is not NULL """, (id,))
        for gcur in gcurs:
            lis.append(gcur)
        cur.close()
        cx.close()
        return lis

    def cal_sell(self,id):
        lis = []
        cx = self.mysql.conn()
        cur = cx.cursor()
        gcurs = cur.execute("""select lot,netprice,price, factorage from fund_sellfund 
where fundid_id =? and lot is not NULL  and netprice is not NULL""", (id,))
        for gcur in gcurs:
            lis.append(gcur)
        cur.close()
        cx.close()
        return  lis