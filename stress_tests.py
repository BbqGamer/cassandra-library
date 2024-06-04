import random
import time

from cassandra_db import CassandraDB
from main import confirm_reservation


def stress_test_1():
    """The client makes the same request very quickly (10000 times)."""
    db = CassandraDB()

    book_id = db.select_all_books()[0].id

    print("Running stress test 1")
    start = time.time()
    for _ in range(10000):
        confirm_reservation(db, [book_id], "tester@gmail.com", True)
    print(f"Finished stress test 1 in: {time.time() - start:.2f} seconds")


def stress_test_2():
    """Two or more clients make the possible requests randomly (10000 times)."""
    db = CassandraDB()

    books = db.select_all_books()

    def random_request(user_email, books):
        num_chosen = random.randint(0, len(books) - 1)
        books_ids = [book.id for book in random.sample(books, num_chosen)]
        confirm_reservation(db, books_ids, user_email, True)

    print("Running stress test 2")
    start = time.time()
    for _ in range(10000 // 2):
        for user_email in ["first@test.com", "second@test.com"]:
            random_request(user_email, books)
    print(f"Finished stress test 2 in: {time.time()-start:.2f} seconds")


if __name__ == "__main__":
    stress_test_1()
    stress_test_2()
