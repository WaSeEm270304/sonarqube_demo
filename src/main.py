# library.py
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import os

class Book:
    def __init__(self, book_id: int, title: str, author: str, isbn: str, copies: int = 1):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.isbn = isbn
        self.total_copies = copies
        self.available_copies = copies
        self.borrowed_by = []  # List of user IDs who borrowed this book

    def __str__(self):
        return f"{self.title} by {self.author} (ID: {self.book_id})"

    def to_dict(self):
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "total_copies": self.total_copies,
            "available_copies": self.available_copies,
            "borrowed_by": self.borrowed_by
        }

    @classmethod
    def from_dict(cls, data):
        book = cls(
            data["book_id"],
            data["title"],
            data["author"],
            data["isbn"],
            data["total_copies"]
        )
        book.available_copies = data["available_copies"]
        book.borrowed_by = data.get("borrowed_by", [])
        return book


class Member:
    def __init__(self, member_id: int, name: str, email: str):
        self.member_id = member_id
        self.name = name
        self.email = email
        self.borrowed_books = []  # List of book_ids
        self.fines = 0.0

    def __str__(self):
        return f"{self.name} (ID: {self.member_id})"

    def to_dict(self):
        return {
            "member_id": self.member_id,
            "name": self.name,
            "email": self.email,
            "borrowed_books": self.borrowed_books,
            "fines": self.fines
        }

    @classmethod
    def from_dict(cls, data):
        member = cls(data["member_id"], data["name"], data["email"])
        member.borrowed_books = data.get("borrowed_books", [])
        member.fines = data.get("fines", 0.0)
        return member


class Library:
    DATA_FILE = "library_data.json"
    FINE_PER_DAY = 1.0  # $1 per day late

    def __init__(self):
        self.books: Dict[int, Book] = {}
        self.members: Dict[int, Member] = {}
        self.next_book_id = 1
        self.next_member_id = 1
        self.borrow_records = {}  # {book_id: {"member_id": int, "due_date": datetime}}
        self.load_data()

    def add_book(self, title: str, author: str, isbn: str, copies: int = 1) -> Book:
        book = Book(self.next_book_id, title, author, isbn, copies)
        self.books[self.next_book_id] = book
        self.next_book_id += 1
        self.save_data()
        print(f"Added: {book}")
        return book

    def search_books(self, query: str) -> List[Book]:
        query = query.lower()
        return [
            book for book in self.books.values()
            if query in book.title.lower() or query in book.author.lower() or query in book.isbn
        ]

    def register_member(self, name: str, email: str) -> Member:
        member = Member(self.next_member_id, name, email)
        self.members[self.next_member_id] = member
        self.next_member_id += 1
        self.save_data()
        print(f"Registered member: {member}")
        return member

    def borrow_book(self, member_id: int, book_id: int, days: int = 14) -> bool:
        if member_id not in self.members:
            print("Member not found!")
            return False
        if book_id not in self.books:
            print("Book not found!")
            return False

        book = self.books[book_id]
        member = self.members[member_id]

        if book.available_copies <= 0:
            print(f"Sorry, '{book.title}' is not available.")
            return False

        if book_id in member.borrowed_books:
            print("You already borrowed this book!")
            return False

        # Borrow the book
        book.available_copies -= 1
        book.borrowed_by.append(member_id)
        member.borrowed_books.append(book_id)

        due_date = datetime.now() + timedelta(days=days)
        self.borrow_records[book_id] = {
            "member_id": member_id,
            "due_date": due_date.isoformat()
        }

        self.save_data()
        print(f"{member.name} borrowed '{book.title}'. Due: {due_date.strftime('%Y-%m-%d')}")
        return True

    def return_book(self, member_id: int, book_id: int) -> bool:
        if member_id not in self.members or book_id not in self.books:
            print("Invalid member or book ID.")
            return False

        member = self.members[member_id]
        book = self.books[book_id]

        if book_id not in member.borrowed_books:
            print("This member didn't borrow this book.")
            return False

        # Return logic
        book.available_copies += 1
        book.borrowed_by.remove(member_id)
        member.borrowed_books.remove(book_id)

        # Check for fine
        if book_id in self.borrow_records:
            record = self.borrow_records[book_id]
            if record["member_id"] == member_id:
                due_date = datetime.fromisoformat(record["due_date"])
                days_late = (datetime.now() - due_date).days
                if days_late > 0:
                    fine = days_late * self.FINE_PER_DAY
                    member.fines += fine
                    print(f"Returned late! Fine: ${fine:.2f}")
                del self.borrow_records[book_id]

        self.save_data()
        print(f"Book returned successfully by {member.name}.")
        return True

    def list_borrowed_books(self, member_id: int) -> List[Book]:
        if member_id not in self.members:
            return []
        member = self.members[member_id]
        return [self.books[bid] for bid in member.borrowed_books if bid in self.books]

    def pay_fine(self, member_id: int, amount: float) -> bool:
        if member_id not in self.members:
            return False
        member = self.members[member_id]
        if amount > member.fines:
            amount = member.fines
        member.fines -= amount
        self.save_data()
        print(f"Paid ${amount:.2f}. Remaining fine: ${member.fines:.2f}")
        return True

    def save_data(self):
        data = {
            "books": {bid: book.to_dict() for bid, book in self.books.items()},
            "members": {mid: member.to_dict() for mid, member in self.members.items()},
            "next_book_id": self.next_book_id,
            "next_member_id": self.next_member_id,
            "borrow_records": {
                bid: {
                    "member_id": rec["member_id"],
                    "due_date": rec["due_date"]
                } for bid, rec in self.borrow_records.items()
            }
        }
        with open(self.DATA_FILE, "w") as f:
            json.dump(data, f, indent=2)

    def load_data(self):
        if not os.path.exists(self.DATA_FILE):
            return
        try:
            with open(self.DATA_FILE, "r") as f:
                data = json.load(f)
                self.books = {int(k): Book.from_dict(v) for k, v in data.get("books", {}).items()}
                self.members = {int(k): Member.from_dict(v) for k, v in data.get("members", {}).items()}
                self.next_book_id = data.get("next_book_id", 1)
                self.next_member_id = data.get("next_member_id", 1)

                # Reload borrow records
                self.borrow_records = {}
                for bid, rec in data.get("borrow_records", {}).items():
                    self.borrow_records[int(bid)] = {
                        "member_id": rec["member_id"],
                        "due_date": rec["due_date"]
                    }
        except Exception as e:
            print(f"Error loading data: {e}")


# Example usage
if __name__ == "__main__":
    lib = Library()
    lib.add_book("Python Crash Course", "Eric Matthes", "978-1593279285", 3)
    lib.add_book("Clean Code", "Robert Martin", "978-0132350886", 2)
    
    member1 = lib.register_member("Alice Johnson", "alice@example.com")
    member2 = lib.register_member("Bob Smith", "bob@example.com")

    lib.borrow_book(member1.member_id, 1)
    lib.borrow_book(member2.member_id, 2)

    print("\nAlice's borrowed books:")
    for book in lib.list_borrowed_books(member1.member_id):
        print(f" - {book}")
