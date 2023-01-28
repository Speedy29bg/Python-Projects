from Tkinter import *
from Book_Scraper.BookScraper import BookScraper
from Filters_Categories_Sort.Sort import Sort
from Filters_Categories_Sort.Categories import Categories
from Controller.Controller import *


class GUI_Tkinter:
    def __init__(self):
        self.root = Tk()
        self.root.title("BookScrapper")
        self.root.geometry("500x500")
        self.create_widgets()
        self.root.mainloop()

    def create_widgets(self):
        self.label1 = Label(self.root, text="Number of books to scrap: ")
        self.label1.grid(row=0, column=0)
        self.entry1 = Entry(self.root)
        self.entry1.grid(row=0, column=1)

        self.label2 = Label(self.root, text="Filtering: ")
        self.label2.grid(row=1, column=0)
        self.entry2 = Entry(self.root)
        self.entry2.grid(row=1, column=1)

        self.label3 = Label(self.root, text="Sorting: ")
        self.label3.grid(row=2, column=0)
        self.entry3 = Entry(self.root)
        self.entry3.grid(row=2, column=1)

        self.label4 = Label(self.root, text="Genres: ")
        self.label4.grid(row=3, column=0)
        self.entry4 = Entry(self.root)
        self.entry4.grid(row=3, column=1)
        
        self.button1 = Button(self.root, text="Start Scrapping", command=self.scrapping)
        self.button1.grid(row=4, column=0)
        
        self.button2 = Button(self.root, text="Exit", command=self.root.destroy)
        self.button2.grid(row=4, column=1)

    def scrapping(self):
        sort = Sort(None)
        categories = Categories(None)
        categories.list_of_all_category()

        start_scr = BookScraper(int(self.entry1.get()), None, categories.links)
        start_scr.scraping()


        for book in start_scr.links_of_all_books:
            start_scr.get_data_for_book(book)

        sort.sorting(start_scr.list_with_books)


        for key in sort.dict_with_sorted_books_lists:
            print(key)
            for book in sort.dict_with_sorted_books_lists[key]:
                print book
