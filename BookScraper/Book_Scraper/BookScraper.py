from Book.Book import Book
from bs4 import BeautifulSoup
import requests
from Filters_Categories_Sort.Filters import Filters
from Link_Builder.LinkBuilder import LinkBuilder


class BookScraper(object):
    list_with_books = []
    links_of_all_books = []

    def __init__(self, num_of_books, filters, links_of_categories):
        self.categories_url = links_of_categories
        self.request_handler = None
        self.soup = None
        self.filters = Filters(filters)
        self.num_of_books = num_of_books

    def scraping(self):
        for link in self.categories_url:
            if self.__get_n_books(link):
                break

    def __get_n_books(self, category_link):
        next_page_link = LinkBuilder(category_link)
        while True:
            self.request_handler = requests.get(next_page_link.category_link)
            self.soup = BeautifulSoup(self.request_handler.text, 'html.parser')
            self.num_of_books = self.__get_all_books_links_on_page(self.num_of_books)
            if self.num_of_books:
                try:
                    href_next_page = self.soup.find('li', class_='next').find('a', href=True)
                    next_page_link.build_next_page_link(href_next_page)
                    print(next_page_link.category_link)
                except AttributeError:
                    return False

            else:
                return True

    def __get_all_books_links_on_page(self, n):
        book_data = self.soup.find_all('li', class_='col-xs-6 col-sm-4 col-md-3 col-lg-3')
        current_number = 0
        for book_url in book_data:
            if current_number < n:
                if self.filters.list_with_filters is None or self.filters.filtering(book_url):
                    link = book_url.find('a', href=True)
                    self.links_of_all_books.append(link['href'])
                    current_number += 1
            else:
                return 0

        return n - current_number

    def get_data_for_book(self, book):
        link_builder = LinkBuilder()
        link_builder.build_book_page_link(book)
        self.request_handler = requests.get(link_builder.category_link)
        self.soup = BeautifulSoup(self.request_handler.text, 'html.parser')
        self.list_with_books.append(Book(self.soup))
