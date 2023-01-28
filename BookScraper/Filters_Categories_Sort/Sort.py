class Sort(object):
    dict_with_sorted_books_lists = {}

    def __init__(self, sorting_list):
        self.sorting_list = sorting_list

    def sorting(self, list_of_books):
        if self.sorting_list is not None:
            for sort in self.sorting_list:
                self.dict_with_sorted_books_lists['Sorted by ' + sort[0] + ' - ' + sort[1]] = self.sort(list_of_books, sort[0], sort[1])

        else:
            self.dict_with_sorted_books_lists['Default sort :'] = self.sort(list_of_books)

    @staticmethod
    def sort(list_of_books, sort_by='title', option='ascending'):
        if option == 'ascending':
            return sorted(list_of_books, key=lambda x: getattr(x, sort_by))
        else:
            return sorted(list_of_books, key=lambda x: getattr(x, sort_by), reverse=True)
