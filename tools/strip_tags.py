import re

"""
过滤HTML中的标签
将HTML中标签等信息去掉
"""


class StripTags(object):

    def __init__(self):
        pass

    def filterTags(self, htmlstr):
        """
        过滤html标签
        :param htmlstr HTML字符串.
        :return:
        """
        # 先过滤CDATA
        re_cdata = re.compile('//<!\[CDATA\[[^>]*//\]\]>', re.I)  # 匹配CDATA
        re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I)  # Script
        re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)  # style
        re_br = re.compile('<br\s*?/?>')  # 处理换行
        re_h = re.compile('</?\w+[^>]*>')  # HTML标签
        re_comment = re.compile('<!--[^>]*-->')  # HTML注释
        s = re_cdata.sub('', htmlstr)  # 去掉CDATA
        s = re_script.sub('', s)  # 去掉SCRIPT
        s = re_style.sub('', s)  # 去掉style
        s = re_br.sub('\n', s)  # 将br转换为换行
        s = re_h.sub('', s)  # 去掉HTML 标签
        s = re_comment.sub('', s)  # 去掉HTML注释
        # 去掉多余的空行
        blank_line = re.compile('\n+')
        s = blank_line.sub('\n', s)
        #去掉空格 小于号 大于号 & 双引号
        special_chars = {'nbsp':'', 'lt':'<', 'gt':'>', 'amp':'&', 'quot':'"'}
        for i in special_chars:
            special = re.compile(r'&'+i+';', re.I)
            s = special.sub(special_chars[i], s)

        return s


    def onlyText(self, html):
        """
        只获取文本信息
        :param html:
        :return:
        """
        regular = re.compile(r'<[^>]+>',re.S)
        txt = regular.sub('', html)
        re_nrt = re.compile('[\n\r\t]+')
        txt = re_nrt.sub('', txt)
        return txt
