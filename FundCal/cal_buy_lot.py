#!/usr/bin/env python
# coding:utf-8
import sql_class
import cal_sell_lot


class CalBuyLot(object):
    def __init__(self):
        self.mysql = sql_class.SqlConnect()
        self.getsellrate =cal_sell_lot.CalSellLot()

    def cal_main(self, id):
        null_buys = self.cal_get_null_buy(id)
        if null_buys:
            for null_buy in null_buys:
                bid = null_buy[0]
                bdate = null_buy[1]
                bprice = null_buy[2]
                get_his_nprice = self.cal_get_his(id, bdate)
                if get_his_nprice:
                    netprice = get_his_nprice[0][0]
                    factorages = self.cal_get_factorage(id, bprice)
                    if factorages:
                        ftype = factorages[0][1]
                        rate = factorages[0][2]
                        factorage = 0
                        if ftype == 'cash':
                            factorage = rate
                        elif ftype == 'rate':
                            factorage = rate /100 * bprice
                        netmoney = 0
                        if ftype == 'cash':
                            netmoney = bprice - rate
                        elif ftype == 'rate':
                            netmoney = bprice / (1 + rate/100)
                        lot = netmoney / netprice
                        self.cal_update_null_buy(bid, netprice, round(lot, 2), round(factorage, 2))
        self.cal_update_sell_goal(id)



    def cal_get_factorage(self, id, bprice):
        lis = []
        cx = self.mysql.conn()
        cur = cx.cursor()
        gcurs = cur.execute("""select scope, ftype,rate from Fund_buyrate 
    where fundid_id =? """, (id,))
        dic = {}
        for index, gcur in enumerate(gcurs):
            dic[index] = gcur[0]
            scope = gcur[0] * 10000
            if scope == 0:
                lis.append(gcur)
            else:
                if bprice < scope:
                    lis.append(gcur)
                    break
                else:
                    if index >= 2:
                        if dic[index] == dic[index - 1]:
                            lis.append(gcur)
        cur.close()
        cx.close()
        return lis

    def cal_update_null_buy(self, bid, netprice, lot, factorage):
        cx = self.mysql.conn()
        cx.execute("""update Fund_buyfund set netprice = ?, lot=? ,factorage=?
    where id =?""", (netprice, lot, factorage, bid))
        cx.commit()
        cx.close()


    def cal_get_null_buy(self, id):
        lis = []
        cx = self.mysql.conn()
        cur = cx.cursor()
        gcurs = cur.execute("""select id, buyDate, price from Fund_buyfund 
    where fundid_id =? and lot is NULL  """, (id,))
        for gcur in gcurs:
            lis.append(gcur)
        cur.close()
        cx.close()
        return lis

    def cal_get_his(self, id, bdate):
        lis = []
        cx = self.mysql.conn()
        cur = cx.cursor()
        gcurs = cur.execute("""select netprice from Fund_hscrapyfund 
    where fundid_id =? and fundDate=? """, (id,bdate))
        for gcur in gcurs:
            lis.append(gcur)
        cur.close()
        cx.close()
        return lis

    def cal_update_sell_goal(self, id):
        cx = self.mysql.conn()
        gcurs = cx.execute("""select t1.id, t1.factorage, t1.lot, t1.netprice, t1.selloverlot, t1.price,
t2.netprice, julianday(t2.fundDate)-julianday(t1.buyDate)
from  fund_buyfund t1 left join fund_hscrapyfund t2 on t1.fundID_id = t2.FundId_id 
where t2.fundDate = (select max(fundDate) from fund_hscrapyfund where FundId_id = ? ) 
and t1.fundID_id = ? """, (id,id))
        for gcur in gcurs:
            bid = gcur[0]
            bfactorage = gcur[1]
            blot = gcur[2]
            bnetprice = gcur[3]
            bselloverlot = gcur[4]
            bprice = gcur[5]
            hnetprice = gcur[6]
            days = gcur[7]
            if bfactorage is None:
                bfactorage = 0
            if bselloverlot is None:
                bselloverlot = 0
            if bprice is None or bprice == 0:
                bprice = blot * bnetprice
            rate = self.getsellrate.cal_get_factorage(id, days)
            if blot is None:
                sellfactorage = 0
                blot = 0
            else:
                sellfactorage = rate * blot * hnetprice
            if bnetprice is None or bnetprice == 0:
                sellrate = 0
                yearrate = 0
            elif days == 0:
                yearrate = 0
                sellrate = (hnetprice - bnetprice - rate) / bnetprice * 100
            else:
                sellrate = (hnetprice - bnetprice - rate)/bnetprice*100
                yearrate = (hnetprice - bnetprice - rate)/bnetprice/days * 365*100
            sellprice = ((blot-bselloverlot)*hnetprice+sellfactorage+bfactorage)-bprice
            cx.execute("""update fund_buyfund set newnetprice = ?, sellfactorage = ?,
sellrate = ?, yearrate = ?, sellprice = ? WHERE id = ?""",(hnetprice, round(sellfactorage,2), round(sellrate,4), round(yearrate,4), round(sellprice,2), bid))
        cx.commit()
        cx.close()
