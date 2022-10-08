#!/usr/bin/env python3
'''
    booksdatasource.py
    Jeff Ondich, 21 September 
    Authors: Sam Hiken and Barry Nwike

    For use in the "books" assignment at the beginning of Carleton's
    CS 257 Software Design class, Fall 2022.
'''

import csv

class Author:
    def __init__(self, surname='', given_name='', birth_year=None, death_year=None, books = []):
        self.surname = surname
        self.given_name = given_name
        self.birth_year = birth_year
        self.death_year = death_year
        self.books = books

    def __eq__(self, other):
        ''' For simplicity, we're going to assume that no two authors have the same name. '''
        return self.surname == other.surname and self.given_name == other.given_name

class Book:
    def __init__(self, title='', publication_year=None, authors=[]):
        ''' Note that the self.authors instance variable is a list of
            references to Author objects. '''
        self.title = title
        self.publication_year = int(publication_year)
        self.authors = authors

    def __eq__(self, other):
        ''' We're going to make the excessively simplifying assumption that
            no two books have the same title, so "same title" is the same
            thing as "same book". '''
        return self.title == other.title

class BooksDataSource:

    def __init__(self, books_csv_file_name):
        ''' The books CSV file format looks like this:

                title,publication_year,author_description

            For example:

                All Clear,2010,Connie Willis (1945-)
                "Right Ho, Jeeves",1934,Pelham Grenville Wodehouse (1881-1975)

            This __init__ method parses the specified CSV file and creates
            suitable instance variables for the BooksDataSource object containing
            a collection of Author objects and a collection of Book objects.
        '''
        #Read each line of the .csv using a loop, and break down the data 
        #create an Author object and a Book object for each line
        #add object to appropriate list
        
        with open(books_csv_file_name) as file:
            csv_reader = csv.reader(file, delimiter=',')
            self.Authors = []
            self.Books = []
            for row in csv_reader:
                is_present = False
                author_list = self.create_author(row)
                book = self.create_book(row, author_list)
                self.Books.append(book)
                for author in author_list:
                    author.books.append(book)
                    if(self.Authors != None):
                        for other_author in self.Authors:
                            if author.__eq__(other_author):
                                is_present = True
                                other_author.books.append(book)
                        if not is_present:
                            self.Authors.append(author)
                    else:
                        self.Authors.append(author)
        self.sort_authors()
        pass

    def authors(self, search_text=None):
        search_result = []
        for author in self.Authors:
            full_name = author.given_name + ' ' + author.surname
            if search_text == None or (search_text) in full_name:
                search_result.append(author)
        
        ''' Returns a list of all the Author objects in this data source whose names contain
            (case-insensitively) the search text. If search_text is None, then this method
            returns all of the Author objects. In either case, the returned list is sorted
            by surname, breaking ties using given name (e.g. Ann Brontë comes before Charlotte Brontë).
        '''
        return search_result

    def books(self, search_text=None, sort_by='title'):
        ''' Returns a list of all the Book objects in this data source whose
            titles contain (case-insensitively) search_text. If search_text is None,
            then this method returns all of the books objects.

            The list of books is sorted in an order depending on the sort_by parameter:

                'year' -- sorts by publication_year, breaking ties with (case-insenstive) title
                'title' -- sorts by (case-insensitive) title, breaking ties with publication_year
                default -- same as 'title' (that is, if sort_by is anything other than 'year'
                            or 'title', just do the same thing you would do for 'title')
        '''
        search_result = []

       
        for book in self.Books:
            if search_text == None or search_text.lower() in book.title.lower():
                search_result.append(book)

        if sort_by == 'year':
            search_result = self.sort_books_year(search_result)
        else:
            search_result = self.sort_books_title(search_result)

        return search_result

    def books_between_years(self, start_year=None, end_year=None):
        ''' Returns a list of all the Book objects in this data source whose publication
            years are between start_year and end_year, inclusive. The list is sorted
            by publication year, breaking ties by title (e.g. Neverwhere 1996 should
            come before Thief of Time 1996).

            If start_year is None, then any book published before or during end_year
            should be included. If end_year is None, then any book published after or
            during start_year should be included. If both are None, then all books
            should be included.
        '''
        results = []
        if start_year == None: 
            start_year = -10000000
        if end_year == None:
            end_year = 1000000000
        book_list = self.sort_books_year(self.Books)
        for book in book_list:
            if book.publication_year >= start_year and book.publication_year <= end_year:
                results.append(book)
        results = self.sort_books_title(results)
        return results
    
    def create_author(self, row):
        '''Reads a line of csv data and parses for information useful to the creation of an Author object 
            Namely a surname, given_name, birth year, and death year
            Then proceeds to create Author objects for every possible author within the line
            Returns a list of Authors created throughout this process
        '''
        name_string = row[2]
        mult_authors = name_string.split(' and ')
        author_list = []
        for name in mult_authors:
            name_list = name.split(' ')
            surname = name_list[len(name_list) - 2]
            given_name = name_list[0]
            n = 1
            while n < len(name_list) - 2:
                given_name = given_name + ' ' + name_list[n]
                n+=1
            range = name_list[len(name_list)-1]
            range = range[1: len(range)-1]
            year_list = range.split('-')
            birth_year = year_list[0]
            death_year = None
            if year_list[1] != '':
                death_year = year_list[1]
            author = Author(surname,given_name,birth_year,death_year,[])
            author_list.append(author)

        return author_list

    def create_book(self, row, author):
        '''With the assumption that there is only a single book per line of csv file,
            Creates a book object using the information read from the line and a previously parsed list of authors
        '''
        title = row[0]
        publish_year = int(row[1])
        authors = author

        book = Book(title, publish_year, authors)
        return book
    
    def sort_authors(self):
        '''Uses the built in comparison operators for Strings 
            in combination with a Bubble Sort to order the various authors
            Returns a sorted list of books based on their names
        '''
        n = 0
        while n < len(self.Authors)-1:
            l = n+1
            while l < len(self.Authors):
                name1 = self.Authors[n].surname
                name2 = self.Authors[l].surname
                if  name1 == name2:
                    name1 = self.Authors[n].given_name
                    name2 = self.Authors[l].given_name 
                if name1 > name2:
                    temp = self.Authors[n]
                    self.Authors[n] = self.Authors[l]
                    self.Authors[l] = temp
                l+=1
            n+=1
    
    def sort_books_title(self, book_list):
        '''Uses the built in comparison operators for Strings 
            in combination with a Bubble Sort to order the various books
            Returns a sorted list of books based on title
        '''       
        n = 0
        while n < len(book_list) -1:
            l = n+1
            while l < len(book_list):
                title1 = book_list[n].title
                title2 = book_list[l].title
                if title1 > title2:
                    temp = book_list[n]
                    book_list[n] = book_list[l]
                    book_list[l] = temp
                l+=1
            n+=1
        return book_list
    
    def sort_books_year(self, book_list):
        '''Uses the built in comparison operators for Strings 
            in combination with a Bubble Sort to order the various books
            Returns a sorted list of books based on year, but sorts by title if years match
        '''
        n = 0
        while n < len(book_list) -1:
            l = n+1
            while l < len(book_list):
                param1 = book_list[n].publication_year
                param2 = book_list[l].publication_year
                if param1 == param2:
                    param1 = book_list[n].title
                    param2 = book_list[l].title
                if param1 > param2:
                    temp = book_list[n]
                    book_list[n] = book_list[l]
                    book_list[l] = temp
                l+=1
            n+=1
        return book_list

            





if __name__ == "__main__":
    source = BooksDataSource("books1.csv")