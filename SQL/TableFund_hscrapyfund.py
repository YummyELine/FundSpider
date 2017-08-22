import sql_class
import datetime
class hscrapyfund(object):
    def __init__(self):
        self.mysql = sql_class.SqlConnect()

    def inserthscrapy(self, Timess, prices, Rates, fundid):
        listTime = []
        yt = datetime.date.today()
        yt2= yt + datetime.timedelta(-4)
        syt = str(yt2)
        yeart = syt[0:5]

        for times in Timess:
            realTime = ''
            i =1
            lenTime = len(times)
            for time in times:
                if i == 1:
                    time = yeart + time
                if i == lenTime:
                    time = time + ' 15:00:00'
                i += 1
                realTime += time
            listTime.append(realTime)
        # print listTime,prices,Rates
        i = 0
        for histime in listTime:
            dontInsert = 0
            cxobj = sql_class.SqlConnect()
            cx = cxobj.conn()
            cur = cx.cursor()
            gcurs = cur.execute("SELECT id FROM Fund_hscrapyfund where FundId_id =? and fundDate=?", (fundid, histime))
            for gcur in gcurs:
                if gcur:
                    dontInsert = 1
            cur.close()
            cx.close()
            # print dontInsert
            if dontInsert == 0:
                cx1 = self.mysql.conn()
                cx1.execute(
                    """insert into Fund_hscrapyfund(fundDate, netPrice, growthRate, FundId_id) VALUES (?,?,?,?)""",
                    (listTime[i],
                     prices[i], Rates[i], fundid))
                cx1.commit()
                cx1.close()
            i += 1

