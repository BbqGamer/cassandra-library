import random
import time
from concurrent.futures import ThreadPoolExecutor

from cassandra_db import CassandraDB
from main import confirm_reservation, display_reservations
from seed import seed

MAX_WORKERS = 10


def stress_1(db):
    """The client makes the same request very quickly (10000 times)."""
    book_id = db.select_all_books()[0].id
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        for _ in range(10000):
            executor.submit(
                confirm_reservation, db, [book_id], "tester@gmail.com", True
            )


def stress_2(db):
    """Two or more clients make the possible requests randomly (10000 times)."""
    books = db.select_all_books()

    def random_request(user_email, books):
        num_chosen = random.randint(0, len(books) - 1)
        books_ids = [book.id for book in random.sample(books, num_chosen)]
        confirm_reservation(db, books_ids, user_email, auto=True)

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        for _ in range(10000 // 2):
            for user_email in ["first@test.com", "second@test.com"]:
                executor.submit(random_request, user_email, books)


def stress_3(db):
    """Immediate occupancy of all seats/reservations by 2 clients.
    Idea is we have one pool for reservation and 2 clients want to claim as much as possible.
    A situation where one client claims all Is undesirable"""
    all_book_ids = [book.id for book in db.select_all_books()]
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        executor.submit(confirm_reservation, db, all_book_ids, "foo", True)
        executor.submit(confirm_reservation, db, all_book_ids, "bar", True)


def run_test(func):
    seed()
    db = CassandraDB()
    start = time.time()

    print(f"\nStarting {func.__name__}")
    func(db)
    print(f"Finished running {func.__name__} in: {time.time()-start:.2f} seconds")
    display_reservations(db)


if __name__ == "__main__":
    run_test(stress_1)
    run_test(stress_2)
    run_test(stress_3)
