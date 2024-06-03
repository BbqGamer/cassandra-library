import uuid
from typing import Optional

from cassandra.cluster import Cluster

from db import DB, Book, Reservation


class CassandraDB(DB):
    def __init__(self):
        cluster = Cluster(
            [("127.0.0.1", 9042), ("127.0.0.1", 9043), ("127.0.0.1", 9044)]
        )
        self.session = cluster.connect()

    def select_all_books(self) -> list[Book]:
        query = "SELECT id, title, author FROM library.books;"
        rows = self.session.execute(query)
        return [Book(*row) for row in rows]

    def select_books_by_ids(self, book_ids) -> list[Book]:
        res = []
        for book_id in book_ids:
            query = "SELECT id, title, author FROM library.books WHERE id = %s"
            row = self.session.execute(query, (book_id,))
            if row:
                res.append(Book(*row[0]))
        return res

    def select_reservation_by_book(self, book_id) -> Optional[Reservation]:
        query = """
        SELECT id, book_id, email FROM library.reservations_by_book WHERE book_id = %s"""
        rows = self.session.execute(query, (book_id,))
        for row in rows:
            return Reservation(*row)

    def select_all_reservations(self) -> list[Reservation]:
        query = "SELECT id, book_id, email FROM library.reservations_by_book"
        rows = self.session.execute(query)
        return [Reservation(*row) for row in rows]

    def select_reservation_by_id(self, res_id) -> Optional[Reservation]:
        query = """
        SELECT id, book_id, email FROM library.reservations WHERE id = %s"""
        rows = self.session.execute(query, (res_id,))
        for row in rows:
            return Reservation(*row)

    # Write methods

    def delete_reservation(self, res_id):
        reservation = self.select_reservation_by_id(res_id)
        if reservation:
            self.session.execute(
                "DELETE FROM library.reservations WHERE id = %s", (res_id,)
            )
            self.session.execute(
                "DELETE FROM library.reservations_by_book WHERE book_id = %s AND id = %s",
                (reservation.book_id, res_id),
            )

    def add_new_reservation(self, book_id, email):
        newresid = uuid.uuid4()
        query = (
            "INSERT INTO library.reservations (id, book_id, email) VALUES (%s, %s, %s)"
        )
        self.session.execute(query, (newresid, book_id, email))
        query = """
        INSERT INTO library.reservations_by_book (book_id, id, email) VALUES (%s, %s, %s)"""
        self.session.execute(query, (book_id, newresid, email))
