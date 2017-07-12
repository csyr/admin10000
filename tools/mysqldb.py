import pymysql
from tools.log import Log


class MySQL(object):

    db_config = {'host':'127.0.0.1', 'user':'root', 'passwd':'', 'db':'blog'}

    def __init__(self):
        try:
            self.conn = None
            self.cur = None
            self.connect()
        except Exception as e:
            pass

    def connect(self):
        """
        链接数据库
        :return:
        """
        if not self.conn:
            self.conn = pymysql.connect(host=self.db_config['host'],user=self.db_config['user'],passwd=self.db_config['passwd'],db=self.db_config['db'], charset='utf8')  # 数据库

        if not self.cur:
            self.cur = self.conn.cursor()

    def execute(self, sql):
        """
        执行SQL
        :param sql:
        :return:
        """
        try:
            if not self.cur:
                self.connect()
            ret = self.cur.execute(sql)  # 执语句行
            self.conn.commit()
            return ret
        except pymysql.Error as e:
            Log().write_file(str(e))
        return False

    def find(self, sql):
        """
        查询
        :param sql:
        :return:
        """
        if not self.cur:
            self.connect()
        self.cur.execute(sql)  # 执语句行

        ret = self.cur.fetchall()

        return ret
