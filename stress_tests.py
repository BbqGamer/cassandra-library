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
    elapsed = time.time() - start
    print(f"Finished stress test 1 in: {elapsed:.2f} seconds")


if __name__ == "__main__":
    stress_test_1()
