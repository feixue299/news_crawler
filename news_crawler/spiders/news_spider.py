from news_crawler.news import News, session
from parsel.csstranslator import css2xpath
import scrapy
import json
from scrapy.http import HtmlResponse
from scrapy.http.response import text
from scrapy import Selector
from lxml.html.clean import Cleaner
import re
from datetime import datetime


class NewsSpider(scrapy.Spider):
    name = "qqnews"
    allowed_domains = ["new.qq.com"]
    start_urls = [
        "https://i.news.qq.com/trpc.qqnews_web.kv_srv.kv_srv_http_proxy/list?sub_srv_id=24hours&srv_id=pc&offset=0&limit=199&strategy=1&ext={%22pool%22:[%22top%22],%22is_filter%22:7,%22check_type%22:true}",
    ]

    def parse(self, response):
        jsonresponse = json.loads(response.text)
        print("""
        >>>>>>>>>>>>>>>
        {}
        >>>>>>>>>>>>>>>>>
        """.format(len(jsonresponse["data"]["list"])))
        
        for news in jsonresponse["data"]["list"]:
            yield scrapy.Request("https://new.qq.com/rain/a/{}".format(news["cms_id"]), callback=self.news_detail)

    def news_detail(self, response):
        cleaner = Cleaner(safe_attrs=[True])
        sel = Selector(text=response.text, type='html')
        ppath = sel.xpath('//html/body/div/div/div/div/p')
        news = News(content="")
        news.title = sel.xpath('////html/body/div/div/div/div/div/text()').extract_first()
        create_date = re.search('"pubtime":( )*"(.*?)"( )*',response.text).group()[10:].strip().strip('"')
        news.create_date = datetime.strptime(create_date, '%Y-%m-%d %H:%M:%S')
        news.source = re.search('"media":( )*"(.*?)"( )*',response.text).group()[8:].strip().strip('"')
        news.source_id = "qq+" + re.search('"cms_id":( )*"(.*?)"( )*',response.text).group()[9:].strip().strip('"')
        
        for p in ppath.extract():
            np = cleaner.clean_html(p)
            news.content += np
        count = session.query(News).filter(News.source_id==news.source_id).first()
        if count == None:
            print("add source_id:{}".format(news.source_id))
            session.add(news)
            session.commit()    
            session.close()

