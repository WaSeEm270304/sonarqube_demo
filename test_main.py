# test_library.py
import unittest
import os
from datetime import datetime, timedelta
from library import Library, Book, Member


class TestLibrarySystem(unittest.TestCase):
    def setUp(self):
        self.lib = Library()
        # Clear any existing data
        if os.path.exists("library_data.json"):
            os.remove("library_data.json")

        # Add test data
        self.book1 = self.lib.add_book("Test Book 1", "Author A", "1234567890", 2)
        self.book2 = self.lib.add_book("Test Book 2", "Author B", "0987654321", 1)
        self.member = self.lib.register_member("John Doe", "john@test.com")

    def test_add_book(self):
        self.assertEqual(len(self.lib.books), 2)
        self.assertIn(self.book1.book_id, self.lib.books)
        self.assertEqual(self.lib.books[self.book1.book_id].title, "Test Book 1")

    def test_register_member(self):
        self.assertIn(self.member.member_id, self.lib.members)
        self.assertEqual(self.lib.members[self.member.member_id].name, "John Doe")

    def test_borrow_book_success(self):
        success = self.lib.borrow_book(self.member.member_id, self.book1.book_id)
        self.assertTrue(success)
        self.assertEqual(self.lib.books[self.book1.book_id].available_copies, 1)
        self.assertIn(self.book1.book_id, self.member.borrowed_books)

    def test_borrow_unavailable_book(self):
        # Borrow all copies
        self.lib.borrow_book(self.member.member_id, self.book2.book_id)
        success = self.lib.borrow_book(self.member.member_id, self.book2.book_id)
        self.assertFalse(success)  # Should fail (no copies left)

    def test_return_book(self):
        self.lib.borrow_book(self.member.member_id, self.book1.book_id)
        success = self.lib.return_book(self.member.member_id, self.book1.book_id)
        self.assertTrue(success)
        self.assertEqual(self.lib.books[self.book1.book_id].available_copies, 2)
        self.assertNotIn(self.book1.book_id, self.member.borrowed_books)

    def test_fine_calculation(self):
        # Borrow a book
        self.lib.borrow_book(self.member.member_id, self.book1.book_id)

        # Manipulate borrow record to simulate late return (7 days late)
        book_id = self.book1.book_id
        due_date = datetime.now() - timedelta(days=7)
        self.lib.borrow_records[book_id]["due_date"] = due_date.isoformat()

        # Return book
        self.lib.return_book(self.member.member_id, book_id)

        # Check fine: 7 days * $1/day = $7
        self.assertAlmostEqual(self.member.fines, 7.0, places=2)

    def test_pay_fine(self):
        self.member.fines = 10.0
        paid = self.lib.pay_fine(self.member.member_id, 7.0)
        self.assertTrue(paid)
        self.assertAlmostEqual(self.member.fines, 3.0)

    def test_search_books(self):
        results = self.lib.search_books("test book")
        self.assertEqual(len(results), 2)

        results = self.lib.search_books("Author A")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].author, "Author A")

    def tearDown(self):
        if os.path.exists("library_data.json"):
            os.remove("library_data.json")


if __name__ == '__main__':
    unittest.main(verbosity=2)
