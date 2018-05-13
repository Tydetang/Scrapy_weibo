#-*- coding:utf-8 -*-

from scrapy import Spider,FormRequest,Request
from weibo.items import WeiboItem,Weibo_userItem
from scrapy.selector import Selector
import sys
import re
import datetime

reload(sys)
sys.setdefaultencoding('utf-8')

class Searchspider(Spider):
    name = "weibo"
    allowed_domains = ["weibo.cn"]
    url = "https://weibo.cn/search/mblog"
    max_page = 3
    keyword = "python"

    def start_requests(self):
        url = '{url}?hideSearchFrame=&keyword={keyword}&page='.format(url=self.url, keyword=self.keyword)
        # print url
        for page in range(1,self.max_page+1):
            now_url = url+str(page)
            data = {
                # 'mp': str(self.max_page),
                'keyword':str(self.keyword),
                'page': str(page)
            }
            yield FormRequest(now_url,callback=self.parse_index,formdata=data)

    def parse_index(self,response):
        weibos = response.xpath('//div[@class="c" and contains(@id,"M_")]')
        print len(weibos)
        for weibo in weibos:
            if weibo.xpath('.//span[@class="cmt"]'):
                url = weibo.xpath(u'.//a[contains(.,"原文")]/@href').extract_first()
            else:
                url = weibo.xpath(u'.//a[contains(.,"评论")]/@href').extract_first()
            yield Request(url,callback=self.parse_detail)
            user_url = weibo.xpath(u'.//a[@class="nk"]/@href').extract_first()
            yield Request(user_url,callback=self.parse_preuserdetail)

    def parse_detail(self,response):
        url = response.url
        item = WeiboItem()
        item['content'] = response.xpath('//div[@class="c" and @id="M_"]//span[@class="ctt"]//text()').extract()
        yield item

    def parse_preuserdetail(self, response):
        detail = response.xpath('//div[@class="u"]/div[@class="tip2"]').extract_first()
        # print detail
        item = Weibo_userItem()
        item['user_fans'] = re.findall(re.compile(u'\u7c89\u4e1d\[(.*?)\]'),detail)[0]
        pre_user_urlid = response.xpath('//div[@class="u"]/div[@class="tip2"]/a[contains(.,"@")]/@href').extract_first()
        # print pre_user_urlid
        user_urlid = re.findall(r'.*?=(\d+)',pre_user_urlid)[0]
        user_infourl = 'https://weibo.cn/'+user_urlid+'/info'
        # print user_infourl
        yield Request(user_infourl,meta={"item":item},callback=self.parse_userinfo)

    def parse_userinfo(self,response):
        item = response.meta["item"]
        selector = Selector(response)
        info =';'.join(selector.xpath('//div[@class="c"]/text()').extract())
        # print info
        item['user_id'] = re.findall(u'\u6635\u79f0:(.*?);',info)[0]  # 昵称
        item['user_age'] = re.findall(u'\u6027\u522b:(.*?);',info)[0]  # 性别
        item['user_city'] = re.findall(u'\u5730\u533a:(.*?);',info)[0]  # 地区（包括省份和城市）
        birthday = re.findall(u'\u751f\u65e5:(.*?);', info)  # 生日
        # print item['user_id']
        if birthday:
            try:
                birthday = datetime.datetime.strptime(birthday[0], "%Y-%m-%d")
                item["user_birthday"] = birthday - datetime.timedelta(hours=8)
            except Exception:
                pass
        yield item