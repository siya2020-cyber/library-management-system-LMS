import csv
import os

from book import Book
from member import Member
from borrow_record import BorrowRecord


class Library:
    """Central controller for the library management system."""

    def __init__(self, name: str, data_dir: str = "data"):
        """
        Initialise the Library instance and load existing data.

        Args:
            name (str): The name of the library.
            data_dir (str): Path to the folder holding CSV data files.
        """
        self.name = name
        self.data_dir = data_dir
        self.books = {}         # book_id -> Book
        self.members = {}       # member_id -> Member
        self.records = {}       # record_id -> BorrowRecord
        self._next_record_num = 1

        # Ensure data directory exists
        os.makedirs(self.data_dir, exist_ok=True)

        # Load data from CSV files at startup
        self._load_books()
        self._load_members()
        self._load_records()

    # ------------------------------------------------------------------
    # Private helpers: file paths
    # ------------------------------------------------------------------

    def _books_path(self):
        return os.path.join(self.data_dir, "books.csv")

    def _members_path(self):
        return os.path.join(self.data_dir, "members.csv")

    def _records_path(self):
        return os.path.join(self.data_dir, "records.csv")

    # ------------------------------------------------------------------
    # File I/O: loading data
    # ------------------------------------------------------------------

    def _load_books(self):
        """Load books from the CSV file into memory."""
        path = self._books_path()
        if not os.path.exists(path):
            return
        try:
            with open(path, newline="", encoding="utf-8") as f:
                reader = csv.reader(f)
                next(reader, None)  # Skip header row
                for row in reader:
                    if len(row) < 6:
                        continue
                    book = Book.from_csv_row(row)
                    self.books[book.book_id] = book
        except OSError as e:
            print(f"Warning: Could not load books file: {e}")

    def _load_members(self):
        """Load members from the CSV file into memory."""
        path = self._members_path()
        if not os.path.exists(path):
            return
        try:
            with open(path, newline="", encoding="utf-8") as f:
                reader = csv.reader(f)
                next(reader, None)  # Skip header row
                for row in reader:
                    if len(row) < 4:
                        continue
                    member = Member.from_csv_row(row)
                    self.members[member.member_id] = member
        except OSError as e:
            print(f"Warning: Could not load members file: {e}")

    def _load_records(self):
        """Load borrow records from the CSV file and restore member state."""
        path = self._records_path()
        if not os.path.exists(path):
            return
        try:
            with open(path, newline="", encoding="utf-8") as f:
                reader = csv.reader(f)
                next(reader, None)  # Skip header row
                for row in reader:
                    if len(row) < 5:
                        continue
                    record = BorrowRecord.from_csv_row(row)
                    self.records[record.record_id] = record
                    self._next_record_num += 1

                    # Restore member's borrowed_book_ids for active loans
                    if not record.is_returned():
                        member = self.members.get(record.member_id)
                        book = self.books.get(record.book_id)
                        if member and record.book_id not in member.borrowed_book_ids:
                            member.borrowed_book_ids.append(record.book_id)
                        # Reduce available copies for unreturned books
                        if book:
                            book.available_copies = max(
                                0, book.available_copies - 1
                            )
        except OSError as e:
            print(f"Warning: Could not load records file: {e}")

    # ------------------------------------------------------------------
    # File I/O: saving data
    # ------------------------------------------------------------------

    def save_books(self):
        """Persist all book data to the CSV file."""
        try:
            with open(self._books_path(), "w", newline="",
                      encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(
                    ["book_id", "title", "author", "genre", "year", "copies"]
                )
                for book in self.books.values():
                    writer.writerow(book.to_csv_row())
        except OSError as e:
            print(f"Error: Could not save books: {e}")

    def save_members(self):
        """Persist all member data to the CSV file."""
        try:
            with open(self._members_path(), "w", newline="",
                      encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(
                    ["member_id", "name", "email", "phone"]
                )
                for member in self.members.values():
                    writer.writerow(member.to_csv_row())
        except OSError as e:
            print(f"Error: Could not save members: {e}")

    def save_records(self):
        """Persist all borrow records to the CSV file."""
        try:
            with open(self._records_path(), "w", newline="",
                      encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(
                    ["record_id", "member_id", "book_id",
                     "borrow_date", "due_date", "return_date"]
                )
                for record in self.records.values():
                    writer.writerow(record.to_csv_row())
        except OSError as e:
            print(f"Error: Could not save records: {e}")

    # ------------------------------------------------------------------
    # Book management
    # ------------------------------------------------------------------

    def add_book(self, book: Book):
        """
        Add a new book to the library collection.

        Args:
            book (Book): The book to add.

        Raises:
            ValueError: If a book with the same ID already exists.
        """
        if book.book_id in self.books:
            raise ValueError(
                f"Book ID '{book.book_id}' already exists."
            )
        self.books[book.book_id] = book
        self.save_books()
        print(f"Book '{book.title}' added successfully.")

    def search_books(self, keyword: str):
        """
        Search books by title, author, or genre (case-insensitive).

        Args:
            keyword (str): The search term.

        Returns:
            list[Book]: A list of matching books.
        """
        keyword = keyword.lower()
        results = [
            book for book in self.books.values()
            if keyword in book.title.lower()
            or keyword in book.author.lower()
            or keyword in book.genre.lower()
        ]
        return results

    def list_books(self):
        """
        Return all books in the collection.

        Returns:
            list[Book]: All books.
        """
        return list(self.books.values())

    # ------------------------------------------------------------------
    # Member management
    # ------------------------------------------------------------------

    def register_member(self, member: Member):
        """
        Register a new library member.

        Args:
            member (Member): The member to register.

        Raises:
            ValueError: If a member with the same ID already exists.
        """
        if member.member_id in self.members:
            raise ValueError(
                f"Member ID '{member.member_id}' already exists."
            )
        self.members[member.member_id] = member
        self.save_members()
        print(f"Member '{member.name}' registered successfully.")

    def find_member(self, member_id: str):
        """
        Retrieve a member by their ID.

        Args:
            member_id (str): The member's ID.

        Returns:
            Member or None: The member if found, otherwise None.
        """
        return self.members.get(member_id)

    def list_members(self):
        """
        Return all registered members.

        Returns:
            list[Member]: All members.
        """
        return list(self.members.values())

    # ------------------------------------------------------------------
    # Borrowing and returning
    # ------------------------------------------------------------------

    def borrow_book(self, member_id: str, book_id: str):
        """
        Process a book borrowing request.

        Args:
            member_id (str): The ID of the borrowing member.
            book_id (str): The ID of the book to borrow.

        Raises:
            ValueError: If the member or book is not found,
                        the book is unavailable, or the member
                        has reached their borrow limit.
        """
        member = self.members.get(member_id)
        if not member:
            raise ValueError(f"Member ID '{member_id}' not found.")

        book = self.books.get(book_id)
        if not book:
            raise ValueError(f"Book ID '{book_id}' not found.")

        if not book.is_available():
            raise ValueError(
                f"No copies of '{book.title}' are currently available."
            )

        if not member.can_borrow():
            raise ValueError(
                f"{member.name} has reached the maximum borrow limit "
                f"({Member.MAX_BORROW_LIMIT} books)."
            )

        # Generate a unique record ID
        record_id = f"R{self._next_record_num:04d}"
        self._next_record_num += 1

        # Update book and member state
        book.borrow_copy()
        member.add_borrowed_book(book_id)

        # Create and store the record
        record = BorrowRecord(record_id, member_id, book_id)
        self.records[record_id] = record

        # Persist changes
        self.save_books()
        self.save_records()

        print(
            f"'{book.title}' borrowed by {member.name}. "
            f"Due: {record.due_date}"
        )

    def return_book(self, member_id: str, book_id: str):
        """
        Process a book return.

        Args:
            member_id (str): The ID of the returning member.
            book_id (str): The ID of the book being returned.

        Raises:
            ValueError: If no active loan is found for this
                        member/book combination.
        """
        # Find the active borrow record for this member and book
        active_record = None
        for record in self.records.values():
            if (record.member_id == member_id
                    and record.book_id == book_id
                    and not record.is_returned()):
                active_record = record
                break

        if not active_record:
            raise ValueError(
                f"No active loan found for member '{member_id}' "
                f"and book '{book_id}'."
            )

        member = self.members.get(member_id)
        book = self.books.get(book_id)

        # Mark the record returned and restore book/member state
        active_record.mark_returned()
        if book:
            book.return_copy()
        if member:
            member.remove_borrowed_book(book_id)

        # Persist changes
        self.save_books()
        self.save_records()

        overdue_msg = ""
        if active_record.days_overdue() > 0:
            overdue_msg = (
                f" (was {active_record.days_overdue()} day(s) overdue)"
            )

        print(
            f"'{book.title if book else book_id}' returned "
            f"by {member.name if member else member_id}.{overdue_msg}"
        )

    # ------------------------------------------------------------------
    # Reporting
    # ------------------------------------------------------------------

    def list_overdue_loans(self):
        """
        Return all borrow records that are currently overdue.

        Returns:
            list[BorrowRecord]: Overdue records.
        """
        return [r for r in self.records.values() if r.is_overdue()]

    def member_loan_history(self, member_id: str):
        """
        Return all borrow records for a given member.

        Args:
            member_id (str): The member's ID.

        Returns:
            list[BorrowRecord]: All records for the member.
        """
        return [
            r for r in self.records.values()
            if r.member_id == member_id
        ]
