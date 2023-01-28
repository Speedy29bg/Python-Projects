import requests
from bs4 import BeautifulSoup

NONE_GROUP_LINK = 'http://books.toscrape.com/catalogue/category/books_1/index.html'
BASE_URL = "http://books.toscrape.com/"


class Categories(object):
    links = []

    def __init__(self, category_list):
        self.category_list = category_list

    def list_of_all_category(self):
        if self.category_list is None:
            self.links.append(NONE_GROUP_LINK)
        else:
            for group in self.category_list:
                self.links.append(self.set_group_link(group))

    @staticmethod
    def set_group_link(category):
        request_handler = requests.get(BASE_URL)
        soup = BeautifulSoup(request_handler.text, 'html.parser')
        categories = soup.find_all('a', href=True)

        for item in categories:
            if item.text.strip() == category:
                return BASE_URL + item['href']
