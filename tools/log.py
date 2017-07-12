#coding=utf-8
import datetime, os


class Log(object):
    __LOG__ = None

    def __init__(self, name=None, path='./'):
        self.name = name
        self.path = path

    def get_file_name(self):
        """
        获取日志文件名
        :return:
        """
        if not self.name:
            now = datetime.datetime.now()
            self.name = now.strftime('%Y-%m-%d-%H') + '.log'

    def get_file_path(self):
        """
        获取文件路径
        :return:
        """
        if self.path == './':
            path = os.getcwd()
            self.path = path

    def write_file(self, content):
        """
        写文件
        :param content:
        :return:
        """
        self.get_file_name()
        self.get_file_path()
        if not os.path.isdir(self.path):
            os.mkdir(self.path)
        file_path = self.path + '/' + self.name
        content = content.strip('\n\r\t')
        content += '\n'
        with open(file_path, 'a') as f:
            f.write(str(content))

