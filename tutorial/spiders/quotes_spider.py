import scrapy
from scrapy.selector import Selector
from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.loader import ItemLoader

from tutorial.items import TutorialItem
from tools.strip_tags import StripTags
from tools.down_file import DownFile
from tools.mongodb import Mongo


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        """
        urls = [
            'http://www.baidu.com/s?ie=utf-8&wd=php7',
            'http://www.baidu.com/s?ie=utf-8&wd=php7',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
        """

        allowed_domains = ['www.admin10000.com']
        start_urls = [
            'http://www.admin10000.com/document/9230.html',
            'http://www.admin10000.com/document/10446.html',
            'http://www.admin10000.com/document/7109.html'
        ]

        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        content = response.body
        page = response.url.split("/")[-1]

        """
        content = Selector(response=response).xpath("//div[@class='body textStyle']").extract()
        if (len(content)):
            content = content[0]
        #踢除标签
        strip = StripTags()
        content = strip.filterTags(content)
        #写文件
        filename = 'quotes-%s' % page
        with open(filename, 'w') as f:
            f.write(str(content))
        self.log('Saved file %s' % filename)
        """

        loader = ItemLoader(item=TutorialItem(), response=response)
        loader.add_xpath('title', "//title/text()")
        loader.add_xpath('content', "//div[@class='body textStyle']")
        data = loader.load_item()

        downFile = DownFile(data['content'][0], 'http://www.admin10000.com')
        downFile.downImgFile()

        mongo = Mongo("articles")
        mongo.setTable("admin10000")
        content = data['content'][0]
        # 踢除标签
        strip = StripTags()
        content = strip.filterTags(content)

        article = {'title':data['title'][0], 'content': content}
        mongo.add(article)
