import csv
import os
import uuid

from cassandra.cluster import Cluster


def seed():
    BOOKS_FILE = "data/books.csv"
    if not os.path.exists(BOOKS_FILE):
        print("Books dataset should be in path: ", BOOKS_FILE)

    cluster = Cluster([("127.0.0.1", 9042), ("127.0.0.1", 9043), ("127.0.0.1", 9044)])
    session = cluster.connect()

    print("Cleaning keyspace")
    session.execute("DROP KEYSPACE IF EXISTS library")

    keyspace_query = """
    CREATE KEYSPACE IF NOT EXISTS library
    WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '3'}
    """
    session.execute(keyspace_query)
    print("Created keyspace")

    books_query = """
    CREATE TABLE IF NOT EXISTS library.books (
        id UUID PRIMARY KEY,
        title TEXT,
        author TEXT
    );
    """

    session.execute(books_query)
    print("Created books table")

    reservations_query = """
    CREATE TABLE IF NOT EXISTS library.reservations (
        id UUID PRIMARY KEY,
        book_id UUID,
        email TEXT
    );
    """

    session.execute(reservations_query)
    print("Created reservations table")

    reservations_by_book_query = """
    CREATE TABLE IF NOT EXISTS library.reservations_by_book (
        book_id UUID,
        id UUID,
        email TEXT,
        PRIMARY KEY (book_id, id)
    );
    """

    session.execute(reservations_by_book_query)
    print("Created reservations by book table")

    print("[SEEDING]")
    with open(BOOKS_FILE, "r") as f:
        cr = csv.reader(f)
        _ = next(cr)
        for row in cr:
            book_id = uuid.uuid4()
            session.execute(
                """INSERT INTO library.books (id, title, author) VALUES (%s, %s, %s)""",
                (book_id, row[0], row[1]),
            )


if __name__ == "__main__":
    seed()
