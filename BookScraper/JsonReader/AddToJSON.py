import json
import requests
from Book_Scraper.BookScraper import BookScraper
from bs4 import BeautifulSoup

BASE_URL = "http://books.toscrape.com/index.html"


class AddToJson(object):

    def __init__(self):
        self.book_data = BookScraper.list_with_books
        self.filename = 'BooksInJSON.json'
        # self.soup = BeautifulSoup(request_handler.text, 'html.parser')

    def info_to_json(self):
        books = {}
        with open(self.filename, 'w') as file_object:
            for book in self.book_data:
                books[book.title] = book.__dict__
            json.dump(books, file_object, indent=4)

    def load_list_with_titles_from_json(self):
        titles = []
        json_file = open(self.filename)
        data = json.load(json_file)
        for book_title in data:
            titles.append(book_title)
        json_file.close()
        return titles

    # def get_titles_from_website(self):
    #     request_handler = requests.get(BASE_URL)
    #     soup = BeautifulSoup(request_handler.text, 'html.parser')
    #     book_data = soup.find_all('li', class_='col-xs-6 col-sm-4 col-md-3 col-lg-3')
    #     titles = []
    #     for book in book_data:
    #         titles.append(book.find('h3').find('a')['title'])
    #     return titles
    #
    # def check_if_json_title_is_in_website(self):
    #
    #     for title in data:
    #         if title not in titles:
    #             print(title)
    #     json_file.close()
