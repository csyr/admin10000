import re
import os
import urllib.request as Request


class DownFile(object):
    """
    下载内容中的文件.文件类型包括 图片 压缩文件 办工文档
    """
    SUFFIX_PIC = ['.jpg', '.jpeg', '.gif', '.png', '.bmp', '.svg']
    SUFFIX_ZIP = ['.zip', '.rar', '.7z', '.gz']
    SUFFIX_OFFICE = ['.doc', '.docx', '.xls', '.xlsx', '.ppt']

    def __init__(self, content, domain):
        self.content = content
        self.domain = domain

    def matchImgTagSrc(self):
        """
        匹配img标签
        :return: list 返回图片标签的列表
        """
        reImg = re.compile(r"<img.*src=[\'\"]?(.*?)[\'\"]?>", re.I)
        return reImg.findall(self.content)

    def getImgPath(self):
        """
        获取图片路径的列表
        :return: list 图片路径
        """
        imgTags = self.matchImgTagSrc()
        imgPath = []
        for item in imgTags:
            if(not re.match(r"^http[s]?:", item)):
                imgPath.append(self.domain + item)
            else:
                imgPath.append(item)

        return imgPath

    def downImgFile(self, path="./files/"):
        """
        把图片下载到本地
        :param path:
        :return: None
        """
        imgFile = self.getImgPath()
        if (isinstance(imgFile, list)):
            try:
                if (path[-1] != '/'):
                    path += '/'
                if (not os.path.exists(path)):
                    os.makedirs(path)
                for img in imgFile:
                    imgName = str(img).split('/')[-1]
                    imgName = path+imgName
                    file = Request.urlopen(img)
                    dataImg = file.read()
                    with open(imgName, 'wb') as code:
                        code.write(dataImg)
            except Exception as e:
                print(e)


