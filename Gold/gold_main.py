#!/usr/bin/env python
# coding:utf-8
from Gold import gold_downloader, gold_parser, insert_Tgold, update_Tgold


class GoldMain(object):
    def __init__(self):
        self.downloader = gold_downloader.HtmlDownloader()
        self.parser = gold_parser.HtmlParser()
        self.insert = insert_Tgold.InsertTGold()
        self.update = update_Tgold.UpdateTGold()


    def craw(self,root_url, mod):
        gold_cont = self.downloader.download(root_url)
        new_data = self.parser.parse(gold_cont,mod)
        self.insert.main(new_data)
        self.update.main()
        # 发邮件代码
