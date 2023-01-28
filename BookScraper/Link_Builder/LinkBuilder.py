import re

BASE_URL = "http://books.toscrape.com/catalogue/"
INDEX = "index.html"
LINK_FORMAT = "../../../"


class LinkBuilder(object):

    def __init__(self, category_link=BASE_URL):
        self.category_link = category_link

    def build_next_page_link(self, link):
        if INDEX in self.category_link:
            self.category_link = self.category_link.replace(INDEX, link['href'])
        else:
            self.category_link = re.sub('page-.+html', link['href'], self.category_link)

    def build_book_page_link(self, link):
        if LINK_FORMAT in link:
            print(self.category_link + link[9:])
            self.category_link = self.category_link + link[9:]
        else:
            print(self.category_link + link[6:])
            self.category_link = self.category_link + link[6:]
