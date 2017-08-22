import sqlite3


class SqlConnect(object):
    def conn(self):
        return sqlite3.connect("D:/PY/DJangoProject/MySite/db.sqlite3")