def display_books(books, book_ids):
    for key in book_ids:
        print(f"{key}: {books[key]['title']} by {books[key]['author']}")
    print()


def select_books(books):
    while True:
        try:
            choices = input("Select books by enetring comma separated list of IDs: ")
            choices = list(map(int, choices.split(",")))

            invalid_choices = []
            for choice in choices:
                if choice not in books:
                    invalid_choices.append(choice)

            if invalid_choices:
                print(f"Books with IDs: ({invalid_choices}) are not availible")
                continue

            return choices
        except ValueError:
            print("Invalid input. Please enter a comma separated list of numbers.")


def confirm_reservation(books, book_choices):
    print()
    print("[Reservation]")
    display_books(books, book_choices)

    while True:
        confirmation = input("Confirm the above reservation? (yes/no)")
        if confirmation == "yes":
            for key in book_choices:
                books.pop(key)

            print(f"Success! You reserved {len(book_choices)} books.")
            break
        elif confirmation == "no":
            print("Purchase cancelled.")
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")


def run():
    books = {
        1: {"title": "1984", "author": "George Orwell"},
        2: {"title": "To Kill a Mockingbird", "author": "Harper Lee"},
        3: {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},
    }

    print("Welcome to the Library System!")
    while True:
        display_books(books, books.keys())
        book_choices = select_books(books)
        confirm_reservation(books, book_choices)
        again = input("Do you want to reserve another book? (yes/no): ").lower()
        if again != "yes":
            print("Thank you for using the Library System. Goodbye!")
            break


if __name__ == "__main__":
    run()
