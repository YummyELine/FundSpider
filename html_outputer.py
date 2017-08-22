#!/usr/bin/env python
# coding:utf-8
import sys
from SQL import TableFund_fund
reload(sys)
sys.setdefaultencoding("utf-8")

class HtmlOutputer(object):
    def __init__(self):
        self.datas = TableFund_fund.allAboutFund_fund()
    def output_html(self):
        datas = self.datas.outputer()
        fout = open('output.html', 'w')
        fout.write("<html>")
        fout.write("<body>")
        fout.write('<table border="1">')
        fout.write('<tr align="center">')
        fout.write("<td><b>基金代码</b></td>")
        fout.write("<td><b>基金名称</b></td>")
        fout.write('<td><b>链接地址</b></td>')
        fout.write("<td><b>净值估价</b></td>")
        fout.write("<td><b>估价时间</b></td>")
        fout.write("<td><b>持有成本</b></td>")
        fout.write("<td><b>持有份额</b></td>")
        fout.write("<td><b>估价金额</b></td>")
        fout.write("</tr>")
        for data in datas:
            fout.write("<tr>")
            fout.write("<td>{0}</td>".format(data['fdm']).encode("utf-8"))
            fout.write("<td>{0}</td>".format(data['name']).encode("utf-8"))
            fout.write('<td><a target="_blank" href="{0}">{1}</a></td>'.format(data['url'],data['url']).encode("utf-8"))
            fout.write("<td>{0}</td>".format(data['nowPrice']).encode("utf-8"))
            fout.write("<td>{0}</td>".format(data['checktime']).encode("utf-8"))
            fout.write("<td>{0}</td>".format(data['positionPrice']).encode("utf-8"))
            fout.write("<td>{0}</td>".format(data['totallot']).encode("utf-8"))
            fout.write("<td>{0}</td>".format(data['totallot']*data['nowPrice']).encode("utf-8"))
            fout.write("</tr>")
        fout.write("</table>")
        fout.write("</body>")
        fout.write("</html>")
        fout.close()
