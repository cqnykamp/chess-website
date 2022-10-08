
import booksdatasource
import sys

def main():
    command = sys.argv[1]
    parameter1 = None
    parameter2 = None
    if(len(sys.argv) > 2):
        parameter1 = sys.argv[2]
        if(len(sys.argv)>3):
            parameter2 = sys.argv[3]
    dataSource = booksdatasource.BooksDataSource("books1.csv")
    if(command == "--author"):
        search_text = parameter1
        list = dataSource.authors(search_text)
        display_author(list)
    elif command == "--book":
        if (parameter1 != '-n'):
            search_text = parameter1
            sort_by = parameter2
            display_book(dataSource.books(search_text, sort_by))
        else:
            display_book(dataSource.books(None, sort_by))

    elif command == "--book_yby":
        if((parameter1 != None and parameter1.isnumeric()) or (parameter2 != None and parameter2.isnumeric())):
            if(parameter1 != None and parameter1.isnumeric()):
                year1 = int(parameter1)
            else:
                year1 = None
            if(parameter2 != None and parameter2.isnumeric()):
                year2 = int(parameter2)
            else:
                year2 = None
            display_book(dataSource.sort_books_year(dataSource.books_between_years(year1, year2)))
        else:
            display_book(dataSource.sort_books_year(dataSource.Books))
            
    else:
        file = open('usage.txt')
        print(file.read())
        file.close()


def display_author(authorList):
    '''Takes a given list of author objects and prints out the contained information in a presentable format'''
    for author in authorList:
        author_name = author.given_name + " " + author.surname
        author_years = ""
        if author.birth_year != None and author.death_year != None:
            author_years = "(" + author.birth_year + "-" + author.death_year + ")"
        elif author.birth_year == None:
            author_years = "(-" + author.death_year + ")"
        else:
            author_years = "(" + author.birth_year + "-)"
        print(author_name + ": " + author_years)
        print_author_books(author)

def print_author_books(author):
    '''Helper method that takes all the books written by a given author
        and prints their titles
    '''
    book_string = ""
    for book in author.books:
        
        book_string = book_string + "\n" + book.title
        
    print(book_string[1:]+"\n")

def display_book(bookList):
    '''Helper method that takes a set of books and prints them out in a presentable format'''
    for book in bookList:
        book_title = book.title
        book_authors = ""
        for author in book.authors:
            book_authors = book_authors + author.given_name + " " + author.surname + ", "
        book_year = str(book.publication_year)
        print(book_title + ": " + book_authors + book_year)

if __name__ == '__main__':
	main()

    