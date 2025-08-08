import scrapy
from ..items import book  # Assuming your item class is named `book`. If it's `Book`, change this.

class BookSpider(scrapy.Spider):
    name = "books"
    start_urls = ['https://books.toscrape.com/']

    def parse(self, response):
        books = response.css('article.product_pod')

        for book_sel in books:
            item = book()
            item['title'] = book_sel.css('h3 a::attr(title)').get()
            item['price'] = book_sel.css('p.price_color::text').get()
            item['availability'] = book_sel.css('p.instock.availability::text').re_first(r'\S+')

            # Extract rating from class (e.g., "star-rating Three")
            classes = book_sel.css('p.star-rating').attrib.get('class', '')
            rating = classes.replace('star-rating', '').strip() if 'star-rating' in classes else None
            item['rating'] = rating

            product_page = book_sel.css('h3 a::attr(href)').get()
            item['product_page'] = response.urljoin(product_page)

            yield item

        # Follow pagination link
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
