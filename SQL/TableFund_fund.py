import sql_class
class allAboutFund_fund(object):
    def __init__(self):
        self.mysql = sql_class.SqlConnect()

    def updatefund(self, Time, price, rate, fundid):
        checkTime = Time

        # print checkTime, price
        cx1 = self.mysql.conn()
        cx1.execute(
            """update Fund_fund set checkTime = ? , nowPrice =?, rate = ? where id =?""", (checkTime, price, rate, fundid))
        cx1.commit()
        cx1.close()

    def selectUrl(self):
        cx = self.mysql.conn()
        cur = cx.cursor()
        gcurs = cur.execute("SELECT id, url FROM Fund_fund  ")
        urls = [gcur for gcur in gcurs]
        cur.close()
        cx.close()
        return urls

    def outputer(self):
        datas = []
        cx = self.mysql.conn()
        cur = cx.cursor()
        gcurs = cur.execute("SELECT fdm, name ,url, totallot, nowPrice, checktime, positionPrice FROM Fund_fund")
        for gcur in gcurs:
            dis = {}
            dis['fdm']= gcur[0]
            dis['name'] = gcur[1]
            dis['url'] = gcur[2]
            dis['totallot'] = gcur[3]
            dis['nowPrice'] = gcur[4]
            dis['checktime'] = gcur[5]
            dis['positionPrice'] = gcur[6]
            datas.append(dis)
        cur.close()
        cx.close()
        return datas