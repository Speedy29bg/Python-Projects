from Book_Parser.BookParser import BookParser
from Book_Scraper.BookScraper import BookScraper
from Filters_Categories_Sort.Sort import Sort
from Filters_Categories_Sort.Categories import Categories
from JsonReader.AddToJSON import AddToJson
from GUI_Tkinter.GUI_Tkinter import GUI_Tkinter


def controller():
    book_parser = BookParser()

    if book_parser.parser.X:
        GUI_Tkinter()
        return

    json_reader = AddToJson()
    sort = Sort(book_parser.parser.sorting)
    categories = Categories(book_parser.parser.genres)

    categories.list_of_all_category()

    book_scraper = BookScraper(book_parser.parser.book_number, book_parser.parser.filtering, categories.links)
    book_scraper.scraping()

    append_to_the_list_with_books(book_scraper)
    sort.sorting(book_scraper.list_with_books)
    print_different_types_of_sorts(sort)

    if book_parser.parser.title_list is None:
        json_reader.info_to_json()
    else:
        print json_reader.load_list_with_titles_from_json()

    print(len(book_scraper.list_with_books))

    print book_parser.parser


def append_to_the_list_with_books(book_scraper):
    for book in book_scraper.links_of_all_books:
        book_scraper.get_data_for_book(book)


def print_different_types_of_sorts(sort):
    for key in sort.dict_with_sorted_books_lists:
        print(key)
        for book in sort.dict_with_sorted_books_lists[key]:
            print book