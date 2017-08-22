#!/usr/bin/env python
# coding:utf-8
import sql_class


class getyesterdayprice(object):
    def __init__(self):
        self.mysql = sql_class.SqlConnect()

    def getprice(self, fundid):
        lis = []
        cx = self.mysql.conn()
        cur = cx.cursor()
        gcurs = cur.execute("""select  funddate, netprice, growthrate from Fund_hscrapyfund 
        where fundid_id =? order by funddate desc LIMIT 1  """, (fundid,))
        for gcur in gcurs:
            lis.append(gcur)
        cur.close()
        cx.close()
        return lis

