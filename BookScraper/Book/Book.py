import re

DICT_FOR_CONVERT = {
    'One': 1,
    'Two': 2,
    'Three': 3,
    'Four': 4,
    'Five': 5

}


def convert_string_to_number(rating):
    return DICT_FOR_CONVERT[rating]


class Book(object):
    def __init__(self, soup):
        self.title = self.set_title(soup)
        self.description = self.set_description(soup)
        self.price = self.set_price(soup)
        self.star_rating = self.set_star_rating(soup)
        self.in_stock = self.set_in_stock(soup)
        self.category = self.set_category(soup)

    @staticmethod
    def set_title(soup):
        try:
            return soup.find('h1').text
        except AttributeError:
            return "N/A"

    @staticmethod
    def set_description(soup):
        try:
            return soup.find('p', class_="").text
        except AttributeError:
            return "N/A"

    @staticmethod
    def set_price(soup):
        try:
            price_string = soup.find('p', class_='price_color').text
            price = float(price_string[2:])
            return price
        except AttributeError:
            return 'N/A'

    @staticmethod
    def set_star_rating(soup):
        try:
            return convert_string_to_number(soup.find('p', class_='star-rating')['class'][1])
        except AttributeError:
            return 'N/A'

    @staticmethod
    def set_in_stock(soup):
        try:
            num = ""
            for index in soup.find('p', class_='instock availability').text:
                if index.isdigit():
                    num = num + index
            return int(num)
        except AttributeError:
            return 'N/A'

    @staticmethod
    def set_category(soup):
        try:
            return soup.find('a', href=re.compile("../category/books//*")).text
        except AttributeError:
            return "N/A"

    def __str__(self):
        return "Title : %s\nStar rating :  %d\nPrice :  %.2f\nIn_stock : %d\nCategory : %s\nDescription : %s\n" % (
            self.title.encode('ascii', 'ignore'), self.star_rating, self.price, self.in_stock, self.category.encode('ascii', 'ignore'),
            self.description.encode('ascii', 'ignore'))
