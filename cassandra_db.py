import uuid
from typing import Optional

from cassandra.cluster import Cluster, Session

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
        query = "SELECT id, title, author FROM library.books WHERE id IN %s"
        rows = self.session.execute(query, book_ids)
        return [Book(*row) for row in rows]

    def select_reservation_by_book(self, book_id) -> Optional[Reservation]:
        query = """
        SELECT id, book_id, email FROM library.reservations_by_book WHERE book_id = %s"""
        row = self.session.execute(query, (book_id,))
        if row:
            return Reservation(*next(row))

    def select_all_reservations(self) -> list[Reservation]:
        query = "SELECT id, book_id, email FROM library.reservations_by_book"
        rows = self.session.execute(query)
        return [Reservation(*row) for row in rows]

    def select_reservation_by_id(self, res_id) -> Reservation:
        query = """
        SELECT id, book_id, email FROM library.reservations_by_book WHERE id = %s"""
        row = self.session.execute(query, res_id)
        return Reservation(*next(row))

    # Write methods

    def delete_reservation(self, res_id):
        rows = self.session.execute(
            "SELECT book_id FROM reservations WHERE id = %s", res_id
        )

        if rows:
            book_id = rows[0].book_id
            self.session.execute("DELETE FROM reservations WHERE id = %s", (res_id))
            self.session.execute(
                "DELETE FROM reservations_by_book WHERE book_id = %s AND id = %s",
                (book_id, res_id),
            )

    def add_new_reservation(self, book_id, email):
        newresid = uuid.uuid4()
        query = "INSERT INTO reservations (id, book_id, email) VALUES (%s, %s, %s)"
        self.session.execute(query, newresid, book_id, email)
        query = """
        INSERT INTO reservations_by_book (book_id, id, email) VALUES (%s, %s, %s)"""
        self.session.execute(query, book_id, newresid, email)
