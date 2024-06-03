from typing import Optional

from db import DB, Book, Reservation


class FakeDB(DB):
    _books: dict
    _reservations: dict
    _reservations_by_book: dict

    def __init__(self):
        self._seed()

    def _seed(self):
        self._books = {
            1: {"title": "1984", "author": "George Orwell"},
            2: {"title": "To Kill a Mockingbird", "author": "Harper Lee"},
            3: {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},
        }

        self._reservations = {1: {"book_id": 2, "email": "foo@bar"}}
        self._reservations_by_book = {2: {"id": 1, "email": "foo@bar"}}

    # Read methods

    def select_all_books(self) -> list[Book]:
        res = []
        for book_id, book in self._books.items():
            res.append(Book(book_id, *book.values()))
        return res

    def select_books_by_ids(self, book_ids) -> list[Book]:
        res = []
        for book_id in book_ids:
            if book_id not in self._books:
                print("Book_id: ", book_id, "Not present")
                exit()

            book = self._books[book_id].values()
            res.append(Book(book_id, *book))
        return res

    def select_reservation_by_book(self, book_id) -> Optional[Reservation]:
        if book_id not in self._reservations_by_book:
            return None
        res = self._reservations_by_book[book_id]
        return Reservation(id=res["id"], book_id=book_id, email=res["email"])

    def select_all_reservations(self) -> list[Reservation]:
        reservations = []
        for res_id, reservation in self._reservations.items():
            reservations.append(Reservation(res_id, *reservation.values()))
        return reservations

    def select_reservation_by_id(self, res_id) -> Reservation:
        return Reservation(res_id, *self._reservations[res_id].values())

    # Write methods

    def delete_reservation(self, res_id):
        book_id = self._reservations[res_id]["book_id"]
        del self._reservations_by_book[book_id]
        del self._reservations[res_id]

    def add_new_reservation(self, book_id, email):
        newreskey = max(self._reservations.keys()) + 1
        self._reservations[newreskey] = {
            "book_id": book_id,
            "email": email,
        }
        self._reservations_by_book[book_id] = {
            "id": newreskey,
            "email": email,
        }
