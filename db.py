from typing import NamedTuple, Optional, Protocol


class Book(NamedTuple):
    id: int
    title: str
    author: str


class Reservation(NamedTuple):
    id: int
    book_id: int
    email: str


class DB(Protocol):
    def select_all_books(self) -> list[Book]:
        ...

    def select_books_by_ids(self, book_ids) -> list[Book]:
        ...

    def select_reservation_by_book(self, book_id) -> Optional[Reservation]:
        ...

    def select_all_reservations(self) -> list[Reservation]:
        ...

    def select_reservation_by_id(self, res_id) -> Reservation:
        ...

    # Write methods

    def delete_reservation(self, res_id):
        ...

    def add_new_reservation(self, book_id, email):
        ...
