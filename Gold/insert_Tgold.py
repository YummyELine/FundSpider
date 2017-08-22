#!/usr/bin/env python
# coding:utf-8

import send_mail
import sql_class


class InsertTGold(object):
    def __init__(self):
        self.mysql = sql_class.SqlConnect()
        self.sendmail = send_mail.sendmail()

    def main(self, lis):
        for li in lis:
            cx = self.mysql.conn()
            dates = cx.execute("""select changedate from  Fund_spdr where changedate = ?""", (li['date'],))
            exist_data = None
            for date in dates:
                exist_data = date
            cx.close()
            if exist_data is None:
                self.insert( li['date'], li['change'], li['total'], li['price'])
                title = 'SPDR基金有变动关注'
                content = '变动日期{0}，变动情况：{1},成交价格：{2}美元/盎司，持有总数:{3}。'.format(li['date'], li['change'], li['price'], li['total'])
                self.sendmail.mail(title, content)

    def insert(self, date, change, total, price):
        cx = self.mysql.conn()
        cx.execute("""insert into Fund_spdr (changedate, change, totallot, price)
        VALUES (?, ?, ?, ?)""", (date, change, total, price))
        cx.commit()
        cx.close()
