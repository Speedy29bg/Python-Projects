# Book scraper

- ## Project Summary


  The purpose of this project is:
    - to get books from a book website
    - then to search by genres and titles
    - also to filter data based on given criterias like availability, rating(1 to 5 stars) and price
    - to sort data by given output like price and raiting in ascending or descending order
    - to read data from json file and  to represent it in tkinter  

 - ##  Requirements
    
    This script uses virtualenv with `python2.7`. 
    To run the script successfully you must have first installed `requests`, `beautifulsoup`, `argparser` and `tkinter` modules

 - ##  Usage



    The script is used to gather data from http://books.toscrape.com. You can write the following command in your terminal:

        python main.py [-h] [-a <allergens>]
                [-b <number of books>] [-g <list of genres>] [-s <output ascending/descending>]
                📝-b 50 -g Science -s rating ascending
                [-b <number of books>] [-g <list of genres>] [-f <priority filters>]
                📝-b 24 -g Classics -f rating <3
                [-g <list of genres>] [-f <priority filters>]
                📝-g Fantasy-f price >30
                [-b <number of books>] [-g <list of genres>] [-f <priority filters>] [-d <keyword>]
                📝-b 60 -g Science -f available =14 -d “book”
                [-g <list of genres>] [-t <book title>]
                📝-g Science -t “Book Title”
                [-X]



    About the optional arguments:

    - b - number of books

    - g - list of genres to search through

    - s - list of sortings (for the output, ascending or descending)

    - f - list of priority filters for which books to exclude from the scrape

    - d - list of keywords to be searched from the description

    - t - title of a book to search for

    - F - list of book titles to search for (from given json)
        
    - X - starts graphic interface tkinter to enter data you want to get from the site

 - ##   Tests

    \-

- ##    Technical Details

   
    To get data from http://books.toscrape.com, the script uses the modules `requests` and `beautifulsoup`. With `requests` the script sends http GET request to the server to receive the necessary information. Then with `beautifulsoup` it creates an object from class BeautifulSoup that has the functionality to search through all the html tags in the site and extract data. To send data to search for, it uses `argparser` module that gets input data from the terminal with different arguments for searching, sorting and filtering. All data is colleced in dictionary. In case we use graphic interface(`tkinter`) the data is stored in json file
## Workflow:

1. When you start the script you will be asked for an input like number of books, list of genres you want to search for, way to sort or filter books or directly to start graphical interface 
2. Based on the input it will get all arguments and process them. If you specify the number of books and genre/genres, it will get n books from given genre/genres, otherwise it will returns all books from specific genre/genres. Its possible to search for title of a book or by keywords from the description
3. Then, if you add arguments for sorting, it will sort the gathered data based on price or rating of the book in ascending or descending order
4. You could add filtering arguments for which books to exclude from the scrape. For example *price < 30*, *rating > 2* or *available=14*

5. At the end an output is given that shows all searched books

