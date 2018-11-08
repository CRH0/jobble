# -*- coding: utf-8 -*-
import scrapy
from ..items import ArticlespiderItem
from scrapy import Request
from urllib import parse
from ..utills.common import get_md5
from scrapy.loader import ItemLoader
from ..items import ArticleItem


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        """
        1.获取文章列表页的文章url并交给解析函数进行具体字段的解析
        2.获取下一页的url并交给scrapy进行下载
        :param response:
        :return:
        """
        # 文章
        post_nodes = response.css('#archive .floated-thumb .post-thumb a')
        for post_node in post_nodes:
            post_url = post_node.css('::attr(href)').extract_first("")
            image_url = post_node.css('img::attr(src)').extract_first("")
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url": image_url},
                          callback=self.parse_detail)
        # 页面
        next_urls = response.css(".next.page-numbers ::attr(href)").extract_first("")
        if next_urls:
            yield Request(url=parse.urljoin(response.url, next_urls), callback=self.parse)

    # 爬取文章具体详情
    def parse_detail(self, response):
        # item = ArticlespiderItem()
        # 通过css选择器解析
        item = ArticleItem()
        front_image_url = response.meta.get('front_image_url', '')
        item['front_image_url'] = [front_image_url]
        item['title'] = response.xpath('//div[@class="entry-header"]/h1/text()').extract_first("")
        # item['title'] = response.css('.entry-header h1::text')
        item['create_time'] = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract_first().replace(
            "·",
            "").strip()
        item['vote'] = response.xpath('//span[contains(@class, "vote-post-up")]//h10/text()').extract_first("")
        bookmark_response = response.xpath('//span[contains(@class,"bookmark-btn")]/text()').re('\d+')
        if bookmark_response:
            item['bookmark'] = bookmark_response[0]
        else:
            item['bookmark'] = 0
        comments_response = response.xpath('//a[@href="#article-comment"]/span/text()').re('\d+')
        if comments_response:
            item['comments'] = comments_response[0]
        else:
            item['comments'] = 0
        content_list = response.xpath('//div[@class="entry"]//text()').extract()
        item['content'] = ','.join(content_list)
        item['url'] = response.url
        item['url_object_id'] = get_md5(response.url)

        # 通过itemloder加载item
        item_loder = ItemLoader(item=item, response=response)
        item_loder.add_css("title", '.entry-header h1::text')
        item_loder.add_xpath('create_time','//p[@class="entry-meta-hide-on-mobile"]/text()')
        item_loder.add_value('front_image_url', response.meta.get('front_image_url', ''))
        item_loder.add_value('url', response.url)
        item_loder.add_value('url_object_id', get_md5(response.url))
        item_loder.add_xpath('content','//div[@class="entry"]//text()')
        item = item_loder.load_item()
        yield item
