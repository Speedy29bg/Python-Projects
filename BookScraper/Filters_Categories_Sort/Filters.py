import requests
from bs4 import BeautifulSoup
from Link_Builder.LinkBuilder import LinkBuilder
from Book.Book import Book, convert_string_to_number


class Filters(object):

    def __init__(self, list_with_filters):
        self.list_with_filters = list_with_filters

    def filtering(self, current_book):
        for current_filter in self.list_with_filters:
            if not self.__select_filter(current_book, current_filter):
                return False
        return True

    def __select_filter(self, current_book, item):
        if item[1] == '<':
            return self.lower_than(self.get_value(current_book, item[0]), int(item[2]))
        elif item[1] == '>':
            return self.bigger_than(self.get_value(current_book, item[0]), int(item[2]))
        else:
            return self.equal(self.get_value(current_book, item[0]), int(item[2]))

    @staticmethod
    def lower_than(filter, number):
        if filter < number:
            return True
        return False

    @staticmethod
    def bigger_than(filter, number):
        if filter > number:
            return True
        return False

    @staticmethod
    def equal(filter, number):
        if filter == number:
            return True
        return False

    def get_value(self, current_book, filter_by):
        if filter_by == 'price':
            return self.get_price(current_book)
        elif filter_by == 'rating':
            return self.get_rating(current_book)
        elif filter_by == 'in_stock':
            return self.get_in_stock(current_book)

    @staticmethod
    def get_price(current_book):
        price_string = current_book.find('p', class_='price_color').text
        price = float(price_string[2:])
        return price

    @staticmethod
    def get_rating(current_book):
        rating = current_book.find('p', class_='star-rating')['class'][1]
        return convert_string_to_number(rating)

    @staticmethod
    def get_in_stock(current_book):
        link_builder = LinkBuilder()
        link = current_book.find('a', href=True)
        link_builder.build_book_page_link(link['href'])
        request_handler = requests.get(link_builder.category_link)
        soup = BeautifulSoup(request_handler.text, 'html.parser')
        book = Book(soup)
        return book.in_stock
