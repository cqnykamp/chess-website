'''
   booksdatasourcetest.py
   Jeff Ondich, 24 September 2021

   modified by Sam Hiken and Barry Nwike 9/24
'''

from booksdatasource import Author, Book, BooksDataSource
import unittest

class BooksDataSourceTester(unittest.TestCase):
	def setUp(self):
		self.data_source = BooksDataSource('books1.csv')

	def tearDown(self):
		pass

	def test_unique_author(self):
		authors = self.data_source.authors('Pratchett')
		self.assertTrue(len(authors) == 1)
		self.assertTrue(authors[0] == Author('Pratchett', 'Terry'))

	def test_all_books(self):
		tiny_data_source = BooksDataSource('tinybooks.csv')
		books = tiny_data_source.books()
		self.assertTrue(books != None)
		self.assertTrue(len(books) == 3)
		self.assertTrue(books[0].title == 'Emma')
		self.assertTrue(books[1].title == 'Neverwhere')
		self.assertTrue(books[2].title == 'Omoo')

	def test_author_eq(self):
		author_1 = Author('Lewis', 'Sinclair', 1885, 1951)
		author_2 = Author('Lewis', 'Sinclair', 1885, 1951)
		author_3 = Author('Austen', 'Jane', 1775, 1817)
		self.assertTrue(author_1.__eq__(author_2))
		self.assertFalse(author_1.__eq__(author_3))

	def test_books_eq(self):
		book_1 = Book('Beloved', 1987)
		book_2 = Book('Good Omens', 1990)
		book_3 = Book('Good Omens', 1990)
		self.assertTrue(book_2.__eq__(book_3))
		self.assertFalse(book_1.__eq__(book_2))

	def test_book_between_years(self):
		tiny_data_source = BooksDataSource('tinybooks.csv')
		books_in_years = tiny_data_source.books_between_years(1814,1816)
		self.assertTrue(books_in_years[0].title == 'Emma')

	def test_bookData_getAuthor(self):
		tiny_data_source = BooksDataSource('tinybooks.csv')
		writers = tiny_data_source.authors("man")
		self.assertTrue(len(writers) == 2)
		self.assertTrue('man' in writers[0].surname)
		self.assertTrue("man" in writers[1].given_name)

	def test_getBooks(self):
		tiny_data_source = BooksDataSource('tinybooks.csv')
		books = tiny_data_source.books("E")
		self.assertTrue(len(books) == 2)
		self.assertTrue(books[0].title == "Emma" )
		self.assertTrue(books[1].title == "Neverwhere")

	def test_year_sort(self):
		tiny_data_source = BooksDataSource('tinybooks.csv')
		books = tiny_data_source.books('m', 'year')
		self.assertTrue(len(books) == 2)
		self.assertTrue(books[0].title == 'Emma')
		self.assertTrue(books[1].title == 'Omoo')

	def test_first_name_sort(self):
		data_source = BooksDataSource('books1.csv')
		authors = data_source.authors('man')
		neil = Author('Gaiman', "Neil", 1960)
		herm = Author('Melville', 'Herman', 1819, 1891)
		self.assertTrue(len(authors) == 2)
		self.assertTrue(authors[0].__eq__(neil))
		self.assertTrue(authors[1].__eq__(herm))

	def test_author_name_order(self):
		data_source = BooksDataSource('tinybooks.csv')
		authors = data_source.authors()
		self.assertTrue(authors[0].surname[0] < authors[1].surname[0])
		self.assertTrue(authors[1].surname[0] < authors[2].surname[0])
		#Could work but only if there are no overlapping first letters

	def test_same_publication_year(self):
		tiny_data_source = BooksDataSource('books1.csv')
		books = tiny_data_source.books_between_years(2010,2010)
		self.assertTrue(books[0].title < books[1].title)



if __name__ == '__main__':
	unittest.main()
