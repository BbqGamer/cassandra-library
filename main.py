from typing import List

from db import DB


def display_books(db: DB, book_ids=None):
    print("[BOOKS]")
    if book_ids is None:
        books = db.select_all_books()
    else:
        books = db.select_books_by_ids(book_ids)

    for book_id, title, author in books:
        status = ""
        reservation = db.get_reservation_by_book(book_id)
        if reservation:
            status = f"[Reserved by {reservation[2]}]"
        print(f"{book_id}: {title} by {author} {status}")
    print()


def display_reservations(db: DB):
    for res_id, reservation in db.reservations.items():
        book = db.books[reservation["book_id"]]
        print(
            f"res_id: {res_id} - {book['title']} - reserved by {reservation['email']}"
        )


def select_books(db: DB):
    while True:
        try:
            choices = input("Select books by enetring comma separated list of IDs: ")
            choices = list(map(int, choices.split(",")))

            invalid_choices = []
            reserved = []
            for choice in choices:
                if choice not in db.books:
                    invalid_choices.append(choice)

                if choice in db.reservations_by_book:
                    reserved.append(choice)

            canreserve = True
            if invalid_choices:
                print(f"Books with IDs: ({invalid_choices}) are not availible")
                canreserve = False

            if reserved:
                print(f"Books with IDs: ({reserved}) are already reserved!")
                canreserve = False

            if not canreserve:
                continue

            return choices
        except ValueError:
            print("Invalid input. Please enter a comma separated list of numbers.")


def cancel_reservation(db: DB, user_email: str, res_id: int):
    if res_id not in db.reservations:
        print(f"Reservation with id {res_id} does not exist!")
        return

    res = db.reservations[res_id]
    if res["email"] != user_email:
        print(f"Reservation with id {res_id} doesn't belong to you")
        return

    book_id = res["book_id"]
    del db.reservations_by_book[book_id]
    del db.reservations[res_id]
    print(f"Reservation with id {res_id} cancelled")


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

            print(f"You reserved {len(book_choices)} books.")
            break
        elif confirmation == "no":
            print("Purchase cancelled.")
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")


def run():
    db = DB()

    print("Welcome to the Library System!")
    logged_user_email = input("Input your email: ")

    while True:
        print(
            "\n1: Make a reservation\n2: View reservations\n3: Cancel reservation\n4: Exit"
        )
        choice = input("Select an option: ")

        if choice == "1":
            display_books(db, db.books.keys())
            book_choices = select_books(db)
            confirm_reservation(db, book_choices, logged_user_email)
        elif choice == "2":
            display_reservations(db)
        elif choice == "3":
            try:
                res_id = int(input("Specify reservation to cancel: "))
                cancel_reservation(db, logged_user_email, res_id)
            except ValueError:
                print("Incorrect reservation id")
        else:
            print("Thank you for using the Library System. Goodbye!")
            exit()


if __name__ == "__main__":
    run()
