from library import Library
from book import Book
from member import Member


def print_header(title: str):
    """Print a formatted section header."""
    print("\n" + "=" * 55)
    print(f"  {title}")
    print("=" * 55)


def print_menu():
    """Display the main menu options."""
    print_header("Gisma City Library - Main Menu")
    print("  1. Add a new book")
    print("  2. Search books")
    print("  3. List all books")
    print("  4. Register a new member")
    print("  5. List all members")
    print("  6. Borrow a book")
    print("  7. Return a book")
    print("  8. View overdue loans")
    print("  9. View member loan history")
    print("  0. Exit")
    print("-" * 55)


def get_input(prompt: str, allow_empty: bool = False):
    """
    Prompt the user for input and strip whitespace.

    Args:
        prompt (str): The prompt string displayed to the user.
        allow_empty (bool): If False, re-prompt until input is given.

    Returns:
        str: The user's input.
    """
    while True:
        value = input(prompt).strip()
        if value or allow_empty:
            return value
        print("  Input cannot be empty. Please try again.")


def handle_add_book(library: Library):
    """Handle the 'Add a new book' menu option."""
    print_header("Add New Book")
    try:
        book_id = get_input("  Book ID (e.g. B001): ")
        title = get_input("  Title: ")
        author = get_input("  Author: ")
        genre = get_input("  Genre: ")
        year_str = get_input("  Publication Year: ")
        copies_str = get_input("  Number of Copies: ")

        year = int(year_str)
        copies = int(copies_str)

        if copies < 1:
            print("  Error: Number of copies must be at least 1.")
            return

        book = Book(book_id, title, author, genre, year, copies)
        library.add_book(book)

    except ValueError as e:
        print(f"  Error: {e}")


def handle_search_books(library: Library):
    """Handle the 'Search books' menu option."""
    print_header("Search Books")
    keyword = get_input("  Enter keyword (title / author / genre): ")
    results = library.search_books(keyword)

    if not results:
        print(f"  No books found matching '{keyword}'.")
    else:
        print(f"\n  Found {len(results)} result(s):\n")
        for book in results:
            print(f"    {book.get_info()}")


def handle_list_books(library: Library):
    """Handle the 'List all books' menu option."""
    print_header("All Books")
    books = library.list_books()
    if not books:
        print("  No books in the system yet.")
    else:
        for book in books:
            print(f"  {book.get_info()}")


def handle_register_member(library: Library):
    """Handle the 'Register a new member' menu option."""
    print_header("Register New Member")
    try:
        member_id = get_input("  Member ID (e.g. M001): ")
        name = get_input("  Full Name: ")
        email = get_input("  Email: ")
        phone = get_input("  Phone: ")

        member = Member(member_id, name, email, phone)
        library.register_member(member)

    except ValueError as e:
        print(f"  Error: {e}")


def handle_list_members(library: Library):
    """Handle the 'List all members' menu option."""
    print_header("All Members")
    members = library.list_members()
    if not members:
        print("  No members registered yet.")
    else:
        for member in members:
            print(f"  {member.get_info()}")


def handle_borrow_book(library: Library):
    """Handle the 'Borrow a book' menu option."""
    print_header("Borrow a Book")
    try:
        member_id = get_input("  Member ID: ")
        book_id = get_input("  Book ID: ")
        library.borrow_book(member_id, book_id)
    except ValueError as e:
        print(f"  Error: {e}")


def handle_return_book(library: Library):
    """Handle the 'Return a book' menu option."""
    print_header("Return a Book")
    try:
        member_id = get_input("  Member ID: ")
        book_id = get_input("  Book ID: ")
        library.return_book(member_id, book_id)
    except ValueError as e:
        print(f"  Error: {e}")


def handle_overdue_loans(library: Library):
    """Handle the 'View overdue loans' menu option."""
    print_header("Overdue Loans")
    overdue = library.list_overdue_loans()
    if not overdue:
        print("  No overdue loans at this time.")
    else:
        print(f"  {len(overdue)} overdue loan(s):\n")
        for record in overdue:
            print(f"    {record.get_info()}")


def handle_loan_history(library: Library):
    """Handle the 'View member loan history' menu option."""
    print_header("Member Loan History")
    try:
        member_id = get_input("  Member ID: ")
        member = library.find_member(member_id)
        if not member:
            print(f"  Member '{member_id}' not found.")
            return
        history = library.member_loan_history(member_id)
        if not history:
            print(f"  No loan history found for {member.name}.")
        else:
            print(f"\n  Loan history for {member.name}:\n")
            for record in history:
                print(f"    {record.get_info()}")
    except ValueError as e:
        print(f"  Error: {e}")


def seed_sample_data(library: Library):
    """
    Add sample books and members if the library is empty.

    This makes it easy to test the system without entering data manually.
    """
    if not library.books:
        sample_books = [
            Book("B001", "Clean Code", "Robert C. Martin",
                 "Programming", 2008, 3),
            Book("B002", "The Pragmatic Programmer", "David Thomas",
                 "Programming", 1999, 2),
            Book("B003", "1984", "George Orwell",
                 "Fiction", 1949, 4),
            Book("B004", "Sapiens", "Yuval Noah Harari",
                 "History", 2011, 2),
            Book("B005", "Introduction to Algorithms", "Thomas Cormen",
                 "Computer Science", 2009, 1),
        ]
        for book in sample_books:
            library.books[book.book_id] = book
        library.save_books()
        print("  [Info] Sample books loaded.")

    if not library.members:
        sample_members = [
            Member("M001", "Alice Johnson", "alice@email.com", "555-0101"),
            Member("M002", "Bob Smith", "bob@email.com", "555-0102"),
            Member("M003", "Carol White", "carol@email.com", "555-0103"),
        ]
        for member in sample_members:
            library.members[member.member_id] = member
        library.save_members()
        print("  [Info] Sample members loaded.")


def main():
    """Main function: initialise the library and run the menu loop."""
    library = Library("Gisma City Library", data_dir="data")
    seed_sample_data(library)

    print("\nWelcome to the Gisma City Library Management System!")

    while True:
        print_menu()
        choice = get_input("  Enter your choice: ", allow_empty=True)

        if choice == "1":
            handle_add_book(library)
        elif choice == "2":
            handle_search_books(library)
        elif choice == "3":
            handle_list_books(library)
        elif choice == "4":
            handle_register_member(library)
        elif choice == "5":
            handle_list_members(library)
        elif choice == "6":
            handle_borrow_book(library)
        elif choice == "7":
            handle_return_book(library)
        elif choice == "8":
            handle_overdue_loans(library)
        elif choice == "9":
            handle_loan_history(library)
        elif choice == "0":
            print("\n  Goodbye! Library data has been saved.\n")
            break
        else:
            print("  Invalid choice. Please enter a number from 0 to 9.")


if __name__ == "__main__":
    main()
