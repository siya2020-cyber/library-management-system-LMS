class Member:
    """Represents a registered library member."""

    MAX_BORROW_LIMIT = 3  # Maximum books a member can borrow at once

    def __init__(self, member_id: str, name: str, email: str, phone: str):
        """
        Initialise a Member instance.

        Args:
            member_id (str): Unique identifier for the member.
            name (str): Full name of the member.
            email (str): Email address of the member.
            phone (str): Contact phone number.
        """
        self.member_id = member_id
        self.name = name
        self.email = email
        self.phone = phone
        self.borrowed_book_ids = []  # List of currently borrowed book IDs

    def can_borrow(self):
        """
        Check if the member is allowed to borrow another book.

        Returns:
            bool: True if the member is below the borrow limit.
        """
        return len(self.borrowed_book_ids) < self.MAX_BORROW_LIMIT

    def add_borrowed_book(self, book_id: str):
        """
        Record a newly borrowed book for this member.

        Args:
            book_id (str): The ID of the book being borrowed.

        Returns:
            bool: True if added successfully, False if limit reached.
        """
        if self.can_borrow():
            self.borrowed_book_ids.append(book_id)
            return True
        return False

    def remove_borrowed_book(self, book_id: str):
        """
        Remove a book from the member's borrowed list upon return.

        Args:
            book_id (str): The ID of the book being returned.

        Returns:
            bool: True if removed successfully, False if book not found.
        """
        if book_id in self.borrowed_book_ids:
            self.borrowed_book_ids.remove(book_id)
            return True
        return False

    def get_info(self):
        """
        Return a formatted string with the member's details.

        Returns:
            str: Human-readable summary of the member.
        """
        borrowed_count = len(self.borrowed_book_ids)
        return (
            f"[{self.member_id}] {self.name} | Email: {self.email} | "
            f"Phone: {self.phone} | Books Borrowed: {borrowed_count}/"
            f"{self.MAX_BORROW_LIMIT}"
        )

    def to_csv_row(self):
        """
        Serialise the member as a list for CSV writing.

        Returns:
            list: Fields in the order expected by the CSV file.
        """
        return [self.member_id, self.name, self.email, self.phone]

    @staticmethod
    def from_csv_row(row: list):
        """
        Create a Member instance from a CSV row.

        Args:
            row (list): A list of string fields from the CSV file.

        Returns:
            Member: A new Member instance.
        """
        return Member(
            member_id=row[0],
            name=row[1],
            email=row[2],
            phone=row[3]
        )
