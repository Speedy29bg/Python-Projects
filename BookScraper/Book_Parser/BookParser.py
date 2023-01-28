import argparse
from JsonReader.AddToJSON import AddToJson
from GUI_Tkinter.GUI_Tkinter import GUI_Tkinter


class BookParser(object):
    def __init__(self):
        self.parser = self.__add_arguments_functionality()


    def __add_arguments_functionality(self):
        parser = argparse.ArgumentParser()
        json_reader = AddToJson()
        parser.add_argument('-b', '--book_number', dest='book_number',default=1000, type=int, help='number of books')
        parser.add_argument('-g', '--genres', dest='genres', nargs='+', help='list of genres')
        parser.add_argument('-d', '--description', dest='descr', nargs='+',
                            help='list of keywords to be searched from the description')
        parser.add_argument('-s', '--sorting', dest='sorting', action='append', nargs=2,
                            help='[rating/price/available/title] [ascending/descending]')
        parser.add_argument('-f', '--filtering', dest='filtering', action='append', nargs=3, default=None,
                            help='[rating/price/available] [[ < / > / = ]int]')
        parser.add_argument('-t', '--title', dest='title', help='title of a book to search for')
        parser.add_argument('-F', '--title_list', type=str, help='search book titles in json file')
        group_1 = parser.add_argument_group('single use arguments')
        group_1.add_argument('-X', action='store_true', help='start tkinter GUI')

        args = parser.parse_args()
        return args

    def __call_GUI(self):
        my_tkinter = GUI_Tkinter()
