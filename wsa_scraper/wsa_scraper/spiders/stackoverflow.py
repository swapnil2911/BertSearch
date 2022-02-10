#Universal Encoder is required in the parent folder before running the scraper
import scrapy
from ..items import QuestionListItem
from datetime import datetime

#Main scraper code
class stackoverflow(scrapy.Spider):
    i = 0
    page_no = 20001
    name = 'stackoverflow'
    start_urls = [
        "https://stackoverflow.com/questions?sort=MostVotes&edited=true&page={}".format(page_no)
    ]

    def parse(self, response):
        base_url = 'https://stackoverflow.com'
        que_set = response.css('div.question-summary')
        for q in que_set:
            self.i += 1
            link = q.css('h3 a::attr(href)').get()
            yield response.follow(url=base_url + link, callback=self.parse_question)
        if self.page_no<40001:
            self.page_no += 1
            yield scrapy.Request(url="https://stackoverflow.com/questions?sort=MostVotes&edited=true&page={}".format(self.page_no), callback=self.parse)

    def parse_question(self, response):
        items = QuestionListItem()

        data = response.css('div.inner-content')
        items['question'] = data.css(
            "div h1 a.question-hyperlink::text").extract_first()
        details = data.css("div.question div.s-prose").extract()
        answers_raw = data.css('#answers')
        
        tags = response.css('a.post-tag::text').extract()
        tags_set = set(tags)
        tags = list(tags_set)
        upvotes =  response.css("div.js-vote-count::text").extract_first()
        
        if answers_raw:
            answers = ''
            raw_data = answers_raw.css("div.s-prose").extract_first()
            for row in raw_data:
                answers = answers + row  

        concat_details = ''
        
        for detail in details:
            concat_details = concat_details + detail
            
        items['details'] = concat_details
        items['answers'] = answers
        items['upvotes'] = upvotes
        items['tags'] = tags
        doc = {
            'question': items['question'],
            'details': items['details'],
            'answers': items['answers'],
            'tags': items['tags'],
            'upvotes':items['upvotes'],
        }

        yield items



