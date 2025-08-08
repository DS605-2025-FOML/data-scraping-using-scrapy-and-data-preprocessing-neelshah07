# quotes_scraper/spiders/quotes_spider.py

import scrapy
from ..items import zenquote 

class QuotesSpider(scrapy.Spider):
    name = "zenquote"  # Unique name for the spider
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
    ]

    def parse(self, response):
        # This method is called to handle the response downloaded for each request made.
        
        # We use CSS selectors to find the HTML elements containing the data.
        all_div_quotes = response.css('div.quote')
        
        # Create an instance of our item
        items = zenquote()

        for quote_div in all_div_quotes:
            # Extract data using CSS selectors
            text = quote_div.css('span.text::text').extract_first()
            author = quote_div.css('.author::text').extract_first()
            tags = quote_div.css('.tag::text').extract()
            
            # Populate the item fields
            items['text'] = text
            items['author'] = author
            items['tags'] = tags

            # Yield the populated item to the Scrapy engine
            yield items

        # Find the 'Next' button link and follow it if it exists
        next_page = response.css('li.next a::attr(href)').get()

        if next_page is not None:
            # The 'response.follow' method handles relative URLs automatically
            yield response.follow(next_page, callback=self.parse)