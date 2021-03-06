# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from items import DingdianxiaoshuoItem

class dingdian(scrapy.Spider):
    name="dingdian"
    allowed_domains=["23us.so"]
    # start_urls = ['http://www.23us.so/top/allvisit_1.html']
    # server_link='http://www.23us.so/top/allvisit_'
    # link_last='.html'

    start_urls = ['https://www.23us.so/modules/article/articlelist.php?fullflag=1&page=1']
    server_link='https://www.23us.so/modules/article/articlelist.php?fullflag=1&page='
    link_last=''

    #从start_requests发送请求
    def start_requests(self):
        yield scrapy.Request(url = self.start_urls[0], callback = self.parse1)


    #获取总排行榜每个页面的链接
    def parse1(self, response):
        items=[]
        res = Selector(response)
        #获取总排行榜小说页码数
        max_num=res.xpath('//*[@id="pagestats"]/text()').extract_first()
        max_num=max_num.split('/')[1]
        print("总排行榜最大页面数为："+max_num)
        #for i in max_num+1:
        # max_num = "1"
        for i in range(18, int(max_num)):
            #构造总排行榜中每个页面的链接
            page_url=self.server_link+str(i+1)+self.link_last
            print(page_url)
            yield scrapy.Request(url=page_url, meta={'items':items},callback=self.parse2,dont_filter=True)
            # yield scrapy.Request(url=page_url,meta={'items':items},callback=self.parse2)

    #访问总排行榜的每个页面
    def parse2(self,response):
        print(response.url)
        items=response.meta['items']
        res=Selector(response)
        #获得页面上所有小说主页链接地址
        novel_urls=res.xpath('//td/a[not(@title)]/@href').extract()
        #获得页面上所有小说的名称
        novel_names=res.xpath('//td/a[not(@title)]/text()').extract()

        page_novel_number=len(novel_urls)
        for index in range(page_novel_number):
            item=DingdianxiaoshuoItem()
            item['novel_name']=novel_names[index]
            item['novel_name'] = trim(item['novel_name'])
            item['novel_url'] =novel_urls[index]
            items.append(item)

        for item in items:
            #访问每个小说主页,传递novel_name
            yield scrapy.Request(url=item['novel_url'],meta = {'item':item},callback = self.parse3)

    #访问小说主页，继续完善item
    def parse3(self, response):
        #接收传递的item
        item=response.meta['item']
        #写入小说类别
        item['novel_family']=response.xpath('//table/tr[1]/td[1]/a/text()').extract_first()
        #写入小说作者
        item['novel_author']=response.xpath('//table/tr[1]/td[2]/text()').extract_first()
        item['novel_author'] = trim(item['novel_author'])
        #写入小说状态
        item['novel_status']=response.xpath('//table/tr[1]/td[3]/text()').extract_first()
        #写入小说最后更新时间
        item['novel_updatetime']=response.xpath('//table/tr[2]/td[3]/text()').extract_first()
        #写入小说全部章节页面
        item['novel_all_section_url']=response.xpath('//p[@class="btnlinks"]/a[1]/@href').extract_first()
        url=response.xpath('//p[@class="btnlinks"]/a[@class="read"]/@href').extract_first()


        #modify by fx
        item['novel_imgurl'] = response.xpath('//img[@style="padding:7px; border:1px solid #E4E4E4; width:120px; height:150px; margin:0 25px 0 15px;"]/@src').extract_first()

        item["novel_description"] = response.xpath('//dd[@style="padding:10px 30px 0 25px;"]/p/text()').extract_first()

        #访问显示有全部章节地址的页面
        print("即将访问"+item['novel_name']+"全部章节地址")
        #yield item
        yield  scrapy.Request(url=url,meta={'item':item},callback=self.parse4)

    #将小说所有章节的地址和名称构造列表存入item
    def parse4(self, response):
        #print("这是parse4")
        #接收传递的item
        item=response.meta['item']
        #这里是一个列表，存放小说所有章节地址
        section_urls=response.xpath('//table/tr/td/a/@href').extract()
        #这里是一个列表，存放小说所有章节名称
        section_names=response.xpath('//table/tr/td/a/text()').extract()

        item["novel_section_urls"]=section_urls
        #计数器
        index=0
        #建立哈希表，存储章节地址和章节名称的对应关系
        section_url_And_section_name=dict(zip(section_urls,section_names))
        #将对应关系，写入item
        item["section_url_And_section_name"]=section_url_And_section_name


        yield item

# def trim(s):
#     if len(s) == 0:
#         return ''
#     if s[:1] == ' ':
#         return trim(s[1:])
#     elif s[-1:] == '':
#         return trim(s[:-1])
#     else:
#         return s


def trim(s):
    return s.lstrip().rstrip()


