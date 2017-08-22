#!/usr/bin/env python
# coding:utf-8
import time

import sql_class
import send_mail



class contentMain(object):
    def __init__(self):
        self.mysql = sql_class.SqlConnect()
        self.sendmail = send_mail.sendmail()

    def main(self, fid):
        operate, title, content = self.remain_base(fid)
        if operate == 'No Operate':
            pass
        else:
            self.sendmail.mail(title,content)

    def remain_base(self, fid):
        # 获取对应ID基本的参数值
        maxprice, minprice, buyFloor = self.get_setting(fid)
        # 判断最后一次是买入还是卖出的
        dealstatus, dealdate = self.get_deal_status(fid)
        # 不同的两种处理方式
        if dealstatus is None:
            operate = 'No Operate'
            title = ''
            content = ''
        else:
            if dealstatus == 'buy':
                operate, title, content = self.cal_buy_deal(fid, dealdate, maxprice, minprice, buyFloor)

            else:
                operate, title, content = self.cal_sell_deal(fid, dealdate, maxprice, minprice, buyFloor)



        return operate, title, content


    def fund_name(self, fid):
            lis = []
            cx = self.mysql.conn()
            cur = cx.cursor()
            gcurs = cur.execute("""select name from Fund_fund 
            where id = ? """, (fid,))
            for gcur in gcurs:
                lis.append(gcur)
            cur.close()
            cx.close()
            fund_name = lis[0][0]
            return fund_name

    def get_setting(self, fid):
            lis = []
            cx = self.mysql.conn()
            cur = cx.cursor()
            gcurs = cur.execute("""select maxprice, minprice, buyFloor  from Fund_settingfund 
            where fundid_id =?  """, (fid,))
            for gcur in gcurs:
                lis.append(gcur)
            cur.close()
            cx.close()
            maxprice = lis[0][0]
            minprice = lis[0][1]
            buyFloor = lis[0][2]
            return maxprice, minprice, buyFloor

    # 这个方法的作用是计算最近一次是做了买入还是卖出，并且获取相相反结果的日期，用于计算时间的的全部买入操作或者全部卖出操作。
    def get_deal_status(self, fid):
        maxsell_list = []
        maxbuy_list = []
        minsell_list = []
        minbuy_list = []
        cx = self.mysql.conn()
        maxselldays = cx.execute("""select selldate  from fund_sellfund 
             where fundid_id =? and netprice is not NULL order by selldate desc limit 1 """, (fid,))
        for maxsellday in maxselldays:
            maxsell_list.append(maxsellday)
        maxbuydays = cx.execute("""select buydate  from fund_buyfund 
                     where fundid_id =? AND netprice is not NULL order by buydate desc limit 1 """, (fid,))
        for maxbuyday in maxbuydays:
            maxbuy_list.append(maxbuyday)
        minselldays = cx.execute("""select selldate  from fund_sellfund 
                     where fundid_id =? and netprice is not NULL order by selldate limit 1 """, (fid,))
        for minsellday in minselldays:
            minsell_list.append(minsellday)
        minbuydays = cx.execute("""select buydate  from fund_buyfund 
                             where fundid_id =? AND netprice is not NULL order by buydate limit 1 """, (fid,))
        for minbuyday in minbuydays:
            minbuy_list.append(minbuyday)
        cx.close()
        if maxsell_list == [] and minbuy_list == []:
            dealstatus = None
            dealdate = None
        else:
            if maxsell_list == []:
                selldate = minbuy_list[0][0]
            else:
                selldate = maxsell_list[0][0]
            if maxbuy_list == []:
                buydate = minsell_list[0][0]
            else:
                buydate = maxbuy_list[0][0]
            if buydate >= selldate:
                dealstatus = 'buy'
                dealdate = selldate
            else:
                dealstatus = 'sell'
                dealdate = buydate

        return dealstatus, dealdate

    def cal_buy_deal(self, fid, dealdate, maxprice, minprice, buyFloor):
        cx = self.mysql.conn()
        cur = cx.cursor()
        gcurs = cur.execute("""select lot, netprice, selloverlot,sellfactorage  from Fund_buyfund 
                   where fundid_id =?  and buydate >= ? and netprice is not NULL order by buydate DESC limit 1""", (fid, dealdate))
        all_lot = 0
        all_money = 0
        all_factorage = 0
        for gcur in gcurs:
            lot = gcur[0]
            netprice = gcur[1]
            selloverlot = gcur[2]
            sellfactorage = gcur[3]
            if lot is None:
                lot = 0
            if netprice is None:
                netprice = 0
            if selloverlot is None:
                selloverlot = 0
            if sellfactorage is None:
                sellfactorage = 0
            all_lot += lot - selloverlot
            all_money += (lot - selloverlot) * netprice
            all_factorage += sellfactorage
        if all_lot == 0:
            all_netprice = 0
        else:
            all_netprice = (all_money - all_factorage)/all_lot
        his = cur.execute("""select netPrice, (julianday(datetime('now', 'localtime')) - julianday(?)) from Fund_hscrapyfund 
                           where fundid_id =? order by funddate desc limit 1""", (dealdate,fid))
        his_netprice =0
        days = 0
        for hi in his:
            his_netprice = hi[0]
            days = hi[1]

        avgs= cur.execute("""select nowprice, positionPrice, totallot from Fund_fund 
                                   where id =? """, (fid, ))
        avg_netprice = 0
        now_netprice = 0
        totallot =0
        for avg in avgs:
            now_netprice = avg[0]
            avg_netprice = avg[1]
            totallot = avg[2]
        cur.close()
        cx.close()
        if all_netprice == 0:
            growth = 0
        else:
            growth = round((now_netprice - all_netprice)/all_netprice * 100, 2)
        if avg_netprice == 0:
            avg_growth =0
        else:
            avg_growth = round((now_netprice-avg_netprice)/avg_netprice * 100, 2)
        yearrate = round(growth / days * 365, 2)
        if all_netprice == 0:
            beforegrowth = 0
        else:
            beforegrowth = round((now_netprice - (all_money / all_lot)) /(all_money / all_lot) * 100, 2)
        if growth >= maxprice:
            operate = 'Sell Lot'
            operatelot = all_lot
            operateAffect = growth
            # 卖出操作后的持仓单价
            if (totallot - operatelot) == 0:
                operateAffect_avg =0
            else:
                avg_sell_priec = (operatelot*now_netprice + totallot * avg_netprice)/(totallot - operatelot)
                operateAffect_avg = round((now_netprice - avg_sell_priec)/avg_sell_priec *100,2)
        elif growth <= minprice:
            operate = 'Buy Money'
            operatelot = all_money * buyFloor / 10
            # 操作后那部分的影响
            operateAffect = round((now_netprice - (
            (all_money + operatelot) / (all_lot + (operatelot / now_netprice)))) / all_netprice * 100, 2)
            # 操作后的持仓单价
            avg_price = (totallot * avg_netprice + operatelot) / (totallot + operatelot / now_netprice)
            if avg_price == 0:
                operateAffect_avg = 0
            else:
                # 操作后的总平均增长率
                operateAffect_avg = (now_netprice - avg_price) / avg_price
        else:
            operate = 'No Operate'
            operatelot = all_lot
            operateAffect = growth
            # 卖出操作后的持仓单价
            if (totallot - operatelot) == 0:
                operateAffect_avg = 0
            else:
                avg_sell_priec = (operatelot * now_netprice + totallot * avg_netprice) / (totallot - operatelot)
                operateAffect_avg = round((now_netprice - avg_sell_priec) / avg_sell_priec * 100, 2)
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # 获取基金名称
        name = self.fund_name(fid)
        title = "关于基金:{0}的{1}操作建议说明，{2}".format(name, operate, now_time)
        content = """基金:{0}建议操作{1}：{2}（卖出为份额，买入为金额）
    原本增长率为：{3}，操作后预计增长率为：{4}
    原本的平均增长率为：{5},操作后的增长率为：{6}
    预计年化率为：{7}
                """.format(name, operate, operatelot, beforegrowth, operateAffect, avg_growth, operateAffect_avg,
                           yearrate)
        self.update_suggest(growth, yearrate, operate, operatelot, fid, operateAffect, avg_growth, beforegrowth,
                            operateAffect_avg, 'buy')
        return operate, title, content

    def cal_sell_deal(self, fid, dealdate, maxprice, minprice, buyFloor):
        cx = self.mysql.conn()
        cur = cx.cursor()
        gcurs = cur.execute("""select lot, netprice, factorage  from Fund_sellfund 
                    where fundid_id =?  and netprice is not NULL order by selldate desc limit 1
        """, (fid,))
        all_lot = 0
        all_money = 0
        all_factorage = 0
        for gcur in gcurs:
            lot = gcur[0]
            netprice = gcur[1]
            factorage = gcur[2]
            if lot is None:
                lot = 0
            if netprice is None:
                netprice = 0
            if factorage is None:
                factorage = 0
            all_lot += lot
            all_money += lot * netprice
            all_factorage += factorage

        all_netprice = (all_money - all_factorage) / all_lot
        his = cur.execute("""select netPrice, (julianday(datetime('now', 'localtime')) - julianday(?)) from Fund_hscrapyfund 
                            where fundid_id =? order by funddate desc limit 1""", (dealdate, fid))
        his_netprice = 0
        days = 0
        for hi in his:
            his_netprice = hi[0]
            days = hi[1]

        avgs = cur.execute("""select nowprice, positionPrice, totallot from Fund_fund 
                                    where id =? """, (fid,))
        avg_netprice = 0
        now_netprice = 0
        totallot = 0
        for avg in avgs:
            now_netprice = avg[0]
            avg_netprice = avg[1]
            totallot = avg[2]
        cur.close()
        cx.close()
        growth = round((now_netprice - all_netprice) / all_netprice * 100, 2)
        if avg_netprice == 0:
            avg_growth = 0
        else:
            avg_growth = round((now_netprice - avg_netprice) / avg_netprice * 100, 2)
        yearrate = round(growth / days * 365, 2)
        beforegrowth = round((avg_netprice - now_netprice)/now_netprice * 100, 2)
        if growth >= maxprice:
            operate = 'Sell Lot'
            operatelot = round(totallot * buyFloor / 20,2)
            newnetprice = (totallot * avg_netprice - operatelot * now_netprice)/(totallot-operatelot)
            operateAffect = round((avg_netprice - newnetprice)/newnetprice*100,2)
            # 卖出操作后的持仓单价
            if (totallot - operatelot) == 0:
                operateAffect_avg =0
            else:
                operateAffect_avg = operateAffect
        elif growth <= minprice:
            operate = 'Buy Money'
            operatelot = all_money
            # 操作后那部分的影响
            if all_netprice == 0:
                operateAffect = 0
            else:
                operateAffect = round((now_netprice - (
                    (all_money + operatelot) / (all_lot + (operatelot / now_netprice)))) / all_netprice * 100, 2)

                # 操作后的持仓单价
            avg_price = (totallot * avg_netprice + operatelot) / (totallot + operatelot / now_netprice)
            if avg_price == 0:
                operateAffect_avg = 0
            else:
                # 操作后的总平均增长率
                operateAffect_avg = round((now_netprice - avg_price) / avg_price * 100,2)
        else:
            operate = 'No Operate'
            operatelot = round(totallot * buyFloor / 20, 2)
            if (totallot - operatelot) == 0:
                newnetprice = 0
            else:
                newnetprice = (totallot * avg_netprice - operatelot * now_netprice) / (totallot - operatelot)
            if newnetprice == 0:
                operateAffect = 0
            else:
                operateAffect = round((avg_netprice - newnetprice) / newnetprice * 100, 2)
            # 卖出操作后的持仓单价
            if (totallot - operatelot) == 0:
                operateAffect_avg = 0
            else:
                operateAffect_avg = operateAffect
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # 获取基金名称
        name = self.fund_name(fid)
        title = "关于基金{0}的{1}操作建议说明，{2}".format(name, operate, now_time)
        "关于基金:{0}的{1}操作建议说明，{2}".format(name, operate, now_time)
        content = """基金:{0}建议操作{1}：{2}（卖出为份额，买入为金额）
    原本增长率为：{3}，操作后预计增长率为：{4}
    原本的平均增长率为：{5},操作后的增长率为：{6}
    预计年化率为：{7}
         """.format(name, operate, operatelot, beforegrowth, operateAffect, avg_growth, operateAffect_avg, yearrate)
        self.update_suggest(growth, yearrate, operate, operatelot, fid, operateAffect, avg_growth, beforegrowth,
                            operateAffect_avg, 'sell')
        return operate, title, content

    def update_suggest(self, growthrate, yearrate, operate, operatelot, fid, operateaffect, avg_growth, growth, operateaffect_avg, lastOpperate):
        cx = self.mysql.conn()
        gcurs = cx.execute("""select id  from Fund_suggestfund 
             where fundid_id =?  """, (fid,))
        suggestID = None
        for gcur in gcurs:
            suggestID = gcur[0]
        if suggestID is None:
            cx.execute("""insert into Fund_suggestfund (growthrate, yearrate, operate, operatelot, fundid_id, operateaffect, avg_growth, growth, operateaffect_avg, lastOpperate)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",(growthrate, yearrate, operate, operatelot, fid, operateaffect, avg_growth, growth, operateaffect_avg, lastOpperate))
        else:
            cx.execute("""update Fund_suggestfund set growthrate = ?, yearrate = ?, operate = ?, operatelot = ?,
 fundid_id = ?, operateaffect = ?, avg_growth = ?, growth = ?, operateaffect_avg = ?, lastOpperate = ? where fundid_id =?  """, (growthrate, yearrate, operate, operatelot, fid, operateaffect, avg_growth, growth, operateaffect_avg, lastOpperate, fid))
        cx.commit()
        cx.close()








