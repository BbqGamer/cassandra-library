class DB:
    books: dict
    reservations: dict
    reservations_by_book: dict

    def __init__(self):
        self._seed()

    def _seed(self):
        self.books = {
            1: {"title": "1984", "author": "George Orwell"},
            2: {"title": "To Kill a Mockingbird", "author": "Harper Lee"},
            3: {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},
        }

        self.reservations = {1: {"book_id": 2, "email": "foo@bar"}}
        self.reservations_by_book = {2: {"id": 1, "email": "foo@bar"}}

    def select_all_books(self):
        res = []
        for book_id in self.books:
            res.append((book_id, *self.books[book_id].values()))
        return res

    def select_books_by_ids(self, book_ids):
        res = []
        for book_id in book_ids:
            res.append((book_id, *self.books[book_id].values()))
        return res

    def get_reservation_by_book(self, book_id):
        if book_id not in self.reservations_by_book:
            return None
        return (book_id, *self.reservations_by_book[book_id].values())
