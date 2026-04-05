class Book:
    """Represents a book in the library collection."""

    def __init__(self, book_id: str, title: str, author: str,
                 genre: str, year: int, copies: int = 1):
        """
        Initialise a Book instance.
        """
        self.book_id = book_id
        self.title = title
        self.author = author
        self.genre = genre
        self.year = year
        self.total_copies = copies
        self.available_copies = copies

    def borrow_copy(self):
        """
        Decrease available copies by one when a book is borrowed.

        Returns:
            bool: True if successful, False if no copies are available.
        """
        if self.available_copies > 0:
            self.available_copies -= 1
            return True
        return False

    def return_copy(self):
        """
        Increase available copies by one when a book is returned.

        Returns:
            bool: True if successful, False if all copies already returned.
        """
        if self.available_copies < self.total_copies:
            self.available_copies += 1
            return True
        return False

    def is_available(self):
        """
        Check whether the book has at least one available copy.

        Returns:
            bool: True if at least one copy is available.
        """
        return self.available_copies > 0

    def get_info(self):
        """
        Return a formatted string with the book's details.

        Returns:
            str: Human-readable summary of the book.
        """
        status = "Available" if self.is_available() else "Not Available"
        return (
            f"[{self.book_id}] '{self.title}' by {self.author} "
            f"({self.year}) | Genre: {self.genre} | "
            f"Copies: {self.available_copies}/{self.total_copies} | {status}"
        )

    def to_csv_row(self):
        """
        Serialise the book as a list for CSV writing.

        Returns:
            list: Fields in the order expected by the CSV file.
        """
        return [
            self.book_id, self.title, self.author,
            self.genre, self.year, self.total_copies
        ]

    @staticmethod
    def from_csv_row(row: list):
        """
        Create a Book instance from a CSV row.

        Args:
            row (list): A list of string fields from the CSV file.

        Returns:
            Book: A new Book instance.
        """
        return Book(
            book_id=row[0],
            title=row[1],
            author=row[2],
            genre=row[3],
            year=int(row[4]),
            copies=int(row[5])
        )
