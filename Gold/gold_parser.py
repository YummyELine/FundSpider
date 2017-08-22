#!/usr/bin/env python
# coding:utf-8
import urlparse

import datetime
from bs4 import BeautifulSoup
import re


class HtmlParser(object):
    def parse(self, html_cont, mod):
        if html_cont is None:
            return
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
        if mod == 'kxt':
            new_data = self._get_new_data(soup)
        elif mod == 'zjw':
            new_data = self.get_zjw_data(soup)
        else:
            new_data = None


        return new_data

    def _get_new_data(self, soup):
        lis = []
        gold_list = soup.find('ul', id="data_list")
        green_golds = gold_list.find_all('li', class_="green")
        for green_gold in green_golds:
            res_data = {}
            date = green_gold.find('span', class_="w210")
            res_data['date'] = date.get_text()
            adds = green_gold.find_all('span', class_="w165")
            res_data['change'] = adds[3].get_text()
            res_data['total'] = adds[1].get_text()
            lis.append(res_data)
            del res_data
        red_golds = gold_list.find_all('li', class_="red")
        for red_gold in red_golds:
            res_data = {}
            date = red_gold.find('span', class_="w210")
            res_data['date'] = date.get_text()
            adds = red_gold.find_all('span', class_="w165")
            res_data['change'] = adds[3].get_text()
            res_data['total'] = adds[1].get_text()
            lis.append(res_data)
        return lis

    def get_zjw_data(self, soup):
        lis = []
        gold_downs = soup.select('.down')
        i = 0
        for gold_down in gold_downs:
            i += 1
            if i%6 == 1:
                res_data = {}
                dates = gold_down.get_text()
                if len(dates) <= 10:
                    datetimeObj = datetime.datetime.strptime(dates, "%Y-%m-%d")
                else:
                    datetimeObj = datetime.datetime.strptime(dates, "%Y-%m-%d %H:%M:%S")
                res_data['date'] = datetimeObj.strftime("%Y-%m-%d %H:%M:%S")


            if i%6 == 2:
                pa = re.compile(r"(\d+\,\d+\.\d+)|(\d+\.\d+)|(\d+)")
                total = pa.match(gold_down.get_text())
                if total:
                    utotals = total.group()
                    rtotal = ''
                    for utotal in utotals:
                        if utotal == ',':
                            pass
                        else:
                            rtotal += utotal
                    res_data['total'] = rtotal
            if i%6 == 3:
                pa = re.compile(r"(-\d+\.\d+)|(-\d+)")
                pa2 = re.compile(r"(-\.\d+)")
                change = pa.search(gold_down.get_text())
                change2 = pa2.search(gold_down.get_text())
                if change:
                    res_data['change'] = change.group()
                if change2:
                    changes = change2.group()
                    rchange = ''
                    for cc in changes:
                        if cc == '.':
                            rchange += '0'
                        rchange += cc
                    res_data['change'] = rchange
            if i%6 == 4:
                pa = re.compile(r"(\d+\,\d+\.\d+)|(\d+\.\d+)|(\d+)")
                price = pa.match(gold_down.get_text())
                if price:
                    uprices = price.group()
                    rprice = ''
                    for uprice in uprices:
                        if uprice == ',':
                            pass
                        else:
                            rprice += uprice
                    res_data['price'] = rprice
                lis.append(res_data)
                del res_data

        gold_ups = soup.select('.up')
        i = 0
        for gold_up in gold_ups:
            i += 1
            if i%6 == 1:
                res_data = {}
                dates = gold_up.get_text()
                if len(dates) <= 10:
                    datetimeObj = datetime.datetime.strptime(dates, "%Y-%m-%d")
                else:
                    datetimeObj = datetime.datetime.strptime(dates, "%Y-%m-%d %H:%M:%S")
                res_data['date'] = datetimeObj.strftime("%Y-%m-%d %H:%M:%S")

            if i%6 == 2:
                pa = re.compile(r"(\d+\,\d+\.\d+)|(\d+\.\d+)|(\d+)")
                total = pa.match(gold_up.get_text())
                if total:
                    utotals = total.group()
                    rtotal = ''
                    for utotal in utotals:
                        if utotal == ',':
                            pass
                        else:
                            rtotal += utotal
                    res_data['total'] = rtotal
            if i%6 == 3:
                pa = re.compile(r"(\d+\.\d+)|(\d+)")
                pa2 = re.compile(r"(\.\d+)")
                change = pa.search(gold_up.get_text())
                change2 = pa2.search(gold_up.get_text())
                if change:
                    res_data['change'] = change.group()
                if change2:
                    changes = change2.group()
                    rchange = ''
                    for cc in changes:
                        if cc == '.':
                            rchange += '0'
                        rchange += cc
                    res_data['change'] = rchange
            if i%6 == 4:
                pa = re.compile(r"(\d+\,\d+\.\d+)|(\d+\.\d+)|(\d+)")
                price = pa.match(gold_up.get_text())
                if price:
                    uprices = price.group()
                    rprice = ''
                    for uprice in uprices:
                        if uprice == ',':
                            pass
                        else:
                            rprice += uprice
                    res_data['price'] = rprice
                lis.append(res_data)
                del res_data
        return lis
