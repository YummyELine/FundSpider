#!/usr/bin/env python
# coding:utf-8
import sql_class
from datetime import datetime



class CalSellLot(object):
    def __init__(self):
        self.mysql = sql_class.SqlConnect()

    def cal_main(self, id):
        null_sells = self.cal_get_null_sell(id)
        if null_sells:
            for null_sell in null_sells:
                sid = null_sell[0]
                sdate = null_sell[1]
                slot = null_sell[2]
                get_his_nprice = self.cal_get_his(id, sdate)
                if get_his_nprice:
                    netprice = get_his_nprice[0][0]
                    # 计算日期+费用
                    factorage = self.count_date(id, sdate, slot)
                    realfactorage = factorage * netprice
                    price = slot * netprice - realfactorage
                    self.cal_update_null_sell(sid, netprice, round(price, 2), round(realfactorage, 2))

    def cal_get_factorage(self, id, countdate):
        lis = []
        cx = self.mysql.conn()
        cur = cx.cursor()
        counts = cur.execute("""select count(scope) from Fund_sellrate
                where fundid_id =? """, (id,))
        cou = 0
        for count in counts:
            cou = count[0]
        gcurs = cur.execute("""select scope, ftype, rate from Fund_sellrate 
        where fundid_id =? """, (id,))
        dic = {}
        for index, gcur in enumerate(gcurs):
            dic[index] = gcur[0]
            scope = gcur[0]
            if countdate == 0 or cou == 1:
                lis.append(gcur)
                break
            else:
                if countdate < scope:
                    lis.append(gcur)
                    break
                else:
                    if index >= 1:
                        if dic[index] == dic[index - 1]:
                            lis.append(gcur)
                            break
        cur.close()
        cx.close()
        rate = lis[0][2] / 100
        return rate

    def cal_update_null_sell(self, sid, netprice, price, factorage):
        cx = self.mysql.conn()
        cx.execute("""update Fund_sellfund set netprice = ?, price=? ,factorage=?
    where id =?""", (netprice, price, factorage, sid))
        cx.commit()
        cx.close()

    def cal_get_null_sell(self, id):
        lis = []
        cx = self.mysql.conn()
        cur = cx.cursor()
        gcurs = cur.execute("""select id, sellDate, lot from Fund_sellfund 
       where fundid_id =? and price is NULL  """, (id,))
        for gcur in gcurs:
            lis.append(gcur)
        cur.close()
        cx.close()
        return lis

    def cal_get_his(self, id, sdate):
        lis = []
        cx = self.mysql.conn()
        cur = cx.cursor()
        gcurs = cur.execute("""select netprice from Fund_hscrapyfund 
       where fundid_id =? and fundDate=? """, (id, sdate))
        for gcur in gcurs:
            lis.append(gcur)
        cur.close()
        cx.close()
        return lis

    def count_date(self, id, sdate, slot):
        lis = []
        factorages = 0
        cx = self.mysql.conn()
        cur = cx.cursor()
        gcurs = cur.execute("""select buydate, lot, selloverlot, id from Fund_buyfund 
               where fundid_id =? and (selloverlot <> lot or selloverlot is NULL  ) order by  buydate  """, (id, ))
        totallot = 0
        # 找出没有被卖过的数据
        for gcur in gcurs:
            lot = gcur[1]
            selloverlot = gcur[2]
            if selloverlot is None:
                selloverlot = 0
            totallot += (lot - selloverlot)
            lis.append(gcur)
            if slot <=  totallot:
                break
        cur.close()
        cx.close()
        # 对符合的数据进行计算
        for li in lis:
            slots = slot
            buydate = li[0]
            lot = li[1]
            selloverlot = li[2]
            bid = li[3]
            if selloverlot is None:
                selloverlot = 0

            slots -= (lot - selloverlot)
            if slots  >= 0:
                slot -= (lot - selloverlot)
                udlot = lot
            else:
                udlot = selloverlot + slot
            fmsdate = datetime.strptime(sdate,"%Y-%m-%d %H:%M:%S")
            fmbdate = datetime.strptime(buydate, "%Y-%m-%d %H:%M:%S")
            countdate = (fmsdate - fmbdate).days
            rate = self.cal_get_factorage(id, countdate)
            factorage = udlot * rate
            factorages += factorage
            cx1 = self.mysql.conn()
            cx1.execute("""update Fund_buyfund set selloverlot =?
               where id =?  """, (udlot, bid ))
            cx1.commit()
            cx1.close()
        return factorages

