import scrapy

from scrapy.spiders import Rule,CrawlSpider
from scrapy.linkextractors import LinkExtractor

from tutorial.items import TutorialItem
from tools.strip_tags import StripTags
from tools.down_file import DownFile
from tools.mongodb import Mongo

from tools.mysqldb import MySQL


class Admin10000Spider(CrawlSpider):
    name = "admin10000"

    allowed_domains = ['www.admin10000.com']
    start_urls = [
        'http://www.admin10000.com/'
    ]

    rules = (
        # 提取匹配 'category.php' (但不匹配 'subsection.php') 的链接并跟进链接(没有callback意味着follow默认为True)
        # Rule(LinkExtractor(allow=('\/document\/\d+\.html', ), deny=('subsection\.php', ))),

        # 提取匹配 'item.php' 的链接并使用spider的parse_item方法进行分析
        Rule(LinkExtractor(allow=('\/document\/\d+\.html', )), callback='parse_item'),
    )

    def parse_item(self, response):

        items = dict()
        items['url'] = response.url
        items['title'] = response.xpath('//title/text()').extract()
        items['content'] = response.xpath("//div[@class='body textStyle']").extract()

        strip = StripTags()
        # 去除标题里的所有标签
        items['title'] = strip.onlyText(items['title'][0])
        # 下载内容里的图片保存到本地
        items['content'] = self.replace_img_src(items['content'][0], "/FILES/"+self.name+"/")

        yield self.save_data(items)

        links = response.xpath('//a/@href').extract()
        for url in links:
            if not self.check_exists(url):
                yield scrapy.Request(url, callback=self.parse_item)

    def check_exists(self, url):
        """
        检查是否已经有记录
        :param url:
        :return:
        """
        mongo = Mongo("articles")
        mongo.setTable("admin10000")
        return mongo.findOne({"url":url})

    def replace_img_src(self, content, path="/FILES/"):
        """
        把内容的图片替换成下载后的图片
        :param content:
        :param path:
        :return:
        """
        downFile = DownFile(content, self.start_urls[0])
        downFile.downImgFile()
        imgs = downFile.matchImgTagSrc()
        for src in imgs:
            imgName = src.split('/')[-1]
            content = content.replace(src, path+imgName)

        return content

    def save_data(self, data):
        """
        保存数据
        :param data:
        :return:
        """
        '''
        mongo = Mongo("articles")
        mongo.setTable("admin10000")
        mongo.add(data)
        '''
        sql = "INSERT INTO `wp_posts` (`ID`, `post_author`, `post_date`, `post_date_gmt`, `post_content`, `post_title`, `post_excerpt`, `post_status`, `comment_status`, `ping_status`, `post_password`, `post_name`, `to_ping`, `pinged`, `post_modified`, `post_modified_gmt`, `post_content_filtered`, `post_parent`, `guid`, `menu_order`, `post_type`, `post_mime_type`, `comment_count`) \
            VALUES(NULL , 1, '2017-04-09 22:39:35', '2017-04-09 14:39:35', '%s', '%s', '', 'inherit', 'closed', 'closed', '', '', '', '', '2017-04-09 22:39:35', '2017-04-09 14:39:35', '', 206, '', 0, 'revision', '', 0);"
        sql = sql % (data['content'], data["title"])
        db = MySQL()
        ret = db.execute(sql)



