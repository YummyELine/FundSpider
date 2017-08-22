#!/usr/bin/env python
# coding:utf-8
import urlparse

import datetime
import time
from bs4 import BeautifulSoup
import re


class HtmlParser(object):
    def parse(self, html_cont):
        if html_cont is None:
            return
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
        new_data = self._get_new_data(soup)
        his_data = self._get_his_data(soup)
        return new_data, his_data

    def now_gold_data(self, html_cont):
        if html_cont is None:
            return
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
        now_gold_data = {}
        nowprice = soup.find('span', class_="nom last")
        if nowprice is None:
            nowprice = soup.find('span', class_="nom last green")
        if nowprice is None:
            nowprice = soup.find('span', class_="nom last red")
        price = float(nowprice.get_text())/100
        now_gold_data['nowPrice'] = price
        time1 = datetime.datetime.now()
        runTimes = time.strptime(str(time1), "%Y-%m-%d %H:%M:%S.%f")
        i = 0
        gYear = None
        for runTime in runTimes:
            if i == 0:
                gYear = runTime
                break
            i += 1
        getTime = soup.find('span', class_="time nowTime")
        textTime = getTime.find('b')
        text_times = textTime.get_text()
        checkTime = str(gYear)+"-"
        for text_time in text_times:
            if text_time == "，":
                pass
            else:
                checkTime += text_time
        now_gold_data['checkTime'] = checkTime
        rates = soup.find('font', class_="swingRange")
        pa = re.compile(r"(-?\d+\.\d+)|(\+?\d+\.\d+)")
        rate = pa.match(rates.get_text())
        if rate:
            now_gold_data['rate'] = rate.group()
        return now_gold_data

    def _get_new_data(self, soup):
        res_data = {}
        nowPrice = soup.find('span', id="gz_gsz")
        res_data['nowPrice'] = nowPrice.get_text()
        Time = soup.find('span', id="gz_gztime")
        Times = Time.get_text()
        checkTime = ''
        for ct in Times:

            if ct == '(':
                ct = '20'
            if ct == ')':
                ct = ':00'
            checkTime += ct
        res_data['checkTime'] = checkTime

        rates = soup.find('span', id="gz_gszzl")
        pa = re.compile(r"(.\d+\.\d+)|(\d+\.\d+)")
        rate = pa.match(rates.get_text())
        if rate:
            res_data['rate'] = rate.group()
        return res_data

    def _get_his_data(self, soup):
        res_data = {}
        data = []

        netDates = soup.find('li', id="Li1").find('table', class_="ui-table-hover").find_all('td', class_="alignLeft")
        for netDate in netDates:
            data.append(netDate.get_text())
        res_data['netDate'] = data

        netPrices = soup.find('li', id="Li1").find('table', class_="ui-table-hover").find_all('td', class_="alignRight bold")
        i = 2
        price = []
        for netPrice in netPrices:
            if i%2 == 0:
                price.append(netPrice.get_text())
            i += 1
        res_data['netPrice'] = price

        Rates = soup.find('li', id="Li1").find('table', class_="ui-table-hover").find_all('td', class_="RelatedInfo alignRight10 bold")
        R = []
        for Rate in Rates:
            rr = Rate.find('span')
            pattern = re.compile(r"(.\d+\.\d+)|(\d+\.\d+)")
            st = pattern.match(rr.get_text())
            if st:
                R.append(st.group())
        res_data['Rate'] = R
        return res_data