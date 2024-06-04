import uuid
from time import sleep
from typing import List

from cassandra_db import CassandraDB
from db import DB

COLOR_RED = "\033[31m"
COLOR_YELLOW = "\033[33m"
COLOR_BLUE = "\033[34m"
COLOR_RESET = "\033[0m"
BOLD = "\033[1m"


def display_books(db: DB, book_ids=None):
    if book_ids is None:
        books = db.select_all_books()
    else:
        books = db.select_books_by_ids(book_ids)

    for book_id, title, author in books:
        text = ""
        reservation = db.select_reservation_by_book(book_id)
        text += f"{COLOR_YELLOW}{book_id}{COLOR_RESET}: {title} by {author}"
        if reservation:
            text = COLOR_RED + text
            text += f" {BOLD}[Reserved by {reservation.email}]{COLOR_RESET}"
        print(text)
    print()


def display_reservations(db: DB, user_email=None):
    reservations = db.select_all_reservations()
    if user_email is not None:
        reservations = list(filter(lambda res: res.email == user_email, reservations))
        if len(reservations) == 0:
            print("[YOU DON'T HAVE ANY RESERVATIONS]")
            return False

    if len(reservations) == 0:
        print("[THERE ARE CURRENTLY NO RESERVATIONS]")
        return False
    print("\n[RESERVATIONS]")
    for reservation in reservations:
        book = db.select_books_by_ids([reservation.book_id])[0]
        print(
            f"{COLOR_BLUE}{reservation.id}{COLOR_RESET} - {book.title} - reserved by {BOLD}{reservation.email}{COLOR_RESET}"
        )
    return True


def select_books(db: DB):
    while True:
        try:
            choices = input(
                f"Select books by enetring comma separated list of {COLOR_YELLOW}book IDs{COLOR_RESET} (or empty list to cancel): "
            )

            if not choices:
                break
            choices = list(map(uuid.UUID, choices.split(",")))

            invalid_choices = []
            reserved = []
            for choice in choices:
                if choice not in {x.id for x in db.select_all_books()}:
                    invalid_choices.append(COLOR_YELLOW + str(choice) + COLOR_RESET)

                if db.select_reservation_by_book(choice) is not None:
                    reserved.append(COLOR_YELLOW + str(choice) + COLOR_RESET)

            canreserve = True
            if invalid_choices:
                print(
                    f"Books with {COLOR_YELLOW}IDs{COLOR_RESET}: ({''.join(invalid_choices)}) are not availible"
                )
                canreserve = False

            if reserved:
                print(
                    f"Books with {COLOR_YELLOW}IDs{COLOR_RESET}: ({''.join(reserved)}) are already reserved!"
                )
                canreserve = False

            if not canreserve:
                continue

            return choices
        except ValueError:
            print("Invalid input. Please enter a comma separated list of book IDs.")


def cancel_reservation(db: DB, user_email: str, res_id: uuid.UUID):
    if res_id not in {res.id for res in db.select_all_reservations()}:
        print(f"Reservation with {COLOR_BLUE}ID:{COLOR_RESET} {res_id} does not exist!")
        return

    reservation = db.select_reservation_by_id(res_id)
    if reservation is None:
        print(f"Reservation with {COLOR_BLUE}ID:{COLOR_RESET} {res_id} doesn't exist")
        return

    if reservation.email != user_email:
        print(
            f"Reservation with {COLOR_BLUE}ID:{COLOR_RESET} {res_id} doesn't belong to you"
        )
        return

    db.delete_reservation(res_id)
    print(f"Reservation with {COLOR_BLUE}ID:{COLOR_RESET} {res_id} cancelled")


def confirm_reservation(db: DB, book_choices: List[uuid.UUID], user_email, auto=False):
    while True:
        if auto:
            confirmation = "yes"
        else:
            confirmation = input("Confirm the above reservation? (yes/no): ")
        if confirmation == "yes" or confirmation == "y":
            reserved = 0
            for key in book_choices:
                success = db.add_new_reservation(key, user_email)
                if success:
                    reserved += 1
            if not auto:
                print(f"You reserved {reserved} books.")
            break
        elif confirmation == "no" or confirmation == "n":
            print("Purchase cancelled.")
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")


def run():
    db = CassandraDB()

    print("Welcome to the Library System!")
    logged_user_email = input("Input your email: ")
    if not logged_user_email:
        print("Email should not be empty")
        exit()

    while True:
        print(
            "\n1: Make a reservation\n2: View reservations\n3: Cancel reservation\n4: Exit"
        )
        choice = input("Select an option: ")

        if choice == "1":
            print("\n[BOOKS]")
            display_books(db)
            book_choices = select_books(db)
            if book_choices:
                print("\n[CHOICES]")
                display_books(db, book_choices)
                confirm_reservation(db, book_choices, logged_user_email)
        elif choice == "2":
            display_reservations(db)
        elif choice == "3":
            has_any = display_reservations(db, logged_user_email)
            if has_any:
                try:
                    res_id = input(
                        f"\nSpecify {COLOR_BLUE}ID{COLOR_RESET} of reservation to remove (or empty string to cancel operation): "
                    )
                    if res_id:
                        cancel_reservation(db, logged_user_email, uuid.UUID(res_id))
                except ValueError:
                    print(f"Incorrect reservation {COLOR_BLUE}UUID{COLOR_RESET}")
        elif choice == "4":
            print("Thank you for using the Library System. Goodbye!")
            exit()
        else:
            print("Incorrect choice - choose value from 1 to 4")


if __name__ == "__main__":
    run()
