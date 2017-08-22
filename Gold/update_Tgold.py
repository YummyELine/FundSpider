#!/usr/bin/env python
# coding:utf-8
import time

import datetime

import sql_class


class UpdateTGold(object):
    def __init__(self):
        self.mysql = sql_class.SqlConnect()

    def main(self):
        cx = self.mysql.conn()
        # 1表示正数，0表示负数
        plus = None
        lc = None
        lt = None
        changeCount = 0
        cd = None
        continueDays = 1
        lp = None
        ifpluss = cx.execute("""select change,continueChange,totallot,changedate,changeCount,continueDays,price from  Fund_spdr where rate is not Null order by changedate desc limit 1""")
        for ifplus in ifpluss:
            lc = ifplus[1]
            lt = ifplus[2]
            cd = datetime.datetime.fromtimestamp(time.mktime(time.strptime(ifplus[3],"%Y-%m-%d %H:%M:%S")))
            changeCount = ifplus[4]
            continueDays = ifplus[5]
            lp = ifplus[6]
            if ifplus[0] > 0:
                plus = 1
            else:
                plus =0

        funds = cx.execute("""select totallot,nowPrice from fund_fund where fdm = '000930'""")
        goldToTal = None
        goldnet = None
        for fund in funds:
            goldToTal = fund[0]
            goldnet = fund[1]

        ratess = cx.execute("""select totallot, change, id, changedate, price from  Fund_spdr where rate is Null order by changedate""")
        for rates in ratess:
            price = rates[4]
            if lp is None:
                changeprice = 0
            else:
                changeprice = price - lp
            lp = price

            totallot = rates[0]
            if lt is None:
                change = rates[1]
            else:
                change = float(totallot) - float(lt)
            lt = totallot
            id = rates[2]
            changedate = datetime.datetime.fromtimestamp(time.mktime(time.strptime(rates[3],"%Y-%m-%d %H:%M:%S")))
            rate = change/totallot
            if change > 0:
                sugOperate = goldToTal * rate * goldnet * 10 * 3
            else:
                sugOperate = goldToTal * rate/10 * 3

            if plus is None:
                # print "空"
                days = 1
                continueDays = days
                cd = changedate
                lc = change
                lt = totallot
                continueChange = change
                continuerate = rate
                changeCount = 1
                if change > 0:
                    plus = 1
                else:
                    plus =0
            elif plus == 1:
                if change > 0:
                    # print "++"
                    changeCount += 1
                    continueChange = change + lc
                    continuerate = continueChange/lt
                    lc = continueChange
                    days = (changedate - cd).total_seconds()
                    continueDays += days
                    cd = changedate
                else:
                    # print "+-"
                    lc = change
                    lt = totallot
                    continueChange = change
                    continuerate = rate
                    plus = 0
                    changeCount = 1
                    days = (changedate - cd).total_seconds()
                    cd = changedate
                    continueDays = days
            else:
                if change > 0:
                    # print '-+'
                    lc = change
                    lt = totallot
                    continueChange = change
                    continuerate = rate
                    plus = 1
                    changeCount = 1
                    days = (changedate - cd).total_seconds()
                    cd = changedate
                    continueDays = days
                else:
                    # print '--'
                    continueChange = change + lc
                    continuerate = continueChange / lt
                    lc = continueChange
                    changeCount += 1
                    days = (changedate - cd).total_seconds()
                    cd = changedate
                    continueDays += days
            cx.execute("""update Fund_spdr set rate=? ,continueChange=?, continuerate=?, changeCount=?, days = ?, continueDays=?, sugOperate=?, change = ?, changeprice = ?
where id=?""", (round(rate*100,2), round(continueChange,2), round(continuerate*100, 2), changeCount, round(days/3600/24, 0), round(continueDays/3600/24, 0), round(sugOperate, 2), round(change,2), round(changeprice,2), id))
        cx.commit()
        cx.close()
