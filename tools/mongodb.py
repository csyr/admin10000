from pymongo.mongo_client import MongoClient
from pymongo.database import Database


class Mongo(object):
    """
    mongo数据库操作
    """
    table = None
    db = None

    def __init__(self, dbName, ip='127.0.0.1', port=27017):
        self.conn(dbName, ip, port)

    def conn(self, dbName, ip, port):
        """
        创建collection
        :param dbName:
        :param ip:
        :param port:
        :return:
        """
        if (isinstance(self.db, Database)):
            return
        try:
            client = MongoClient(ip, port)
            self.db = client[dbName]
        except Exception as e:
            print(e)

    def setTable(self, table):
        table = str(table)
        if (table):
            self.table = table

    def add(self, data, table = None):
        """
        添加数据
        :param data:
        :param table:
        :return:
        """
        if (table):
            self.setTable(table)
        return self.db[self.table].insert(data)

    def findOne(self, where, table=None):
        """
        查询一条记录
        :param where:
        :param table:
        :return:
        """
        if (table):
            self.setTable(table)
        data = self.db[self.table].find(where)
        if isinstance(data, list):
            return data[0]
        return data

    def remove(self, data, table):
        """
        删除数据
        :param data:
        :param table:
        :return:
        """
        table = self.setTable(table)
        if (not table):
            return False
        return self.db[table].remove()