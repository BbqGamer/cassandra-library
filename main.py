from typing import List, NamedTuple


class DB(NamedTuple):
    books: dict
    reservations: dict
    reservations_by_book: dict


def display_books(db: DB, book_ids):
    for key in book_ids:
        status = ""
        if key in db.reservations_by_book:
            status = f"[Borrowed by {db.reservations_by_book[key]['email']}]"
        print(f"{key}: {db.books[key]['title']} by {db.books[key]['author']} {status}")
    print()


def select_books(db: DB):
    while True:
        try:
            choices = input("Select books by enetring comma separated list of IDs: ")
            choices = list(map(int, choices.split(",")))

            invalid_choices = []
            borrowed = []
            for choice in choices:
                if choice not in db.books:
                    invalid_choices.append(choice)

                if choice in db.reservations_by_book:
                    borrowed.append(choice)

            canborrow = True
            if invalid_choices:
                print(f"Books with IDs: ({invalid_choices}) are not availible")
                canborrow = False

            if borrowed:
                print(f"Books with IDs: ({borrowed}) are already borrowed!")
                canborrow = False

            if not canborrow:
                continue

            return choices
        except ValueError:
            print("Invalid input. Please enter a comma separated list of numbers.")


def confirm_reservation(db: DB, book_choices: List[int], user_email):
    print()
    print("[Reservation]")
    display_books(db, book_choices)

    while True:
        confirmation = input("Confirm the above reservation? (yes/no): ")
        if confirmation == "yes":
            for key in book_choices:
                newreskey = max(db.reservations.keys()) + 1
                db.reservations[newreskey] = {"book_id": key, "email": user_email}
                db.reservations_by_book[key] = {"id": newreskey, "email": user_email}

            print(f"Success! You reserved {len(book_choices)} books.")
            break
        elif confirmation == "no":
            print("Purchase cancelled.")
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")


def seed() -> DB:
    books = {
        1: {"title": "1984", "author": "George Orwell"},
        2: {"title": "To Kill a Mockingbird", "author": "Harper Lee"},
        3: {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},
    }

    reservations = {1: {"book_id": 2, "email": "foo@bar"}}
    reservations_by_book = {2: {"id": 1, "email": "foo@bar"}}

    return DB(books, reservations, reservations_by_book)


def run():
    db = seed()

    print("Welcome to the Library System!")
    logged_user_email = input("Input your email: ")

    while True:
        display_books(db, db.books.keys())
        book_choices = select_books(db)
        confirm_reservation(db, book_choices, logged_user_email)
        again = input("Do you want to reserve another book? (yes/no): ").lower()
        if again != "yes":
            print("Thank you for using the Library System. Goodbye!")
            break


if __name__ == "__main__":
    run()
