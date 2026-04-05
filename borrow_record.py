from datetime import date, timedelta


class BorrowRecord:
    """Represents a single borrowing transaction."""

    LOAN_PERIOD_DAYS = 14  # Standard loan period

    def __init__(self, record_id: str, member_id: str, book_id: str,
                 borrow_date: str = None, due_date: str = None,
                 return_date: str = None):
        """
        Initialise a BorrowRecord instance.
        """
        self.record_id = record_id
        self.member_id = member_id
        self.book_id = book_id

        # Default borrow date to today if not provided
        if borrow_date:
            self.borrow_date = date.fromisoformat(borrow_date)
        else:
            self.borrow_date = date.today()

        # Default due date to borrow_date + LOAN_PERIOD_DAYS
        if due_date:
            self.due_date = date.fromisoformat(due_date)
        else:
            self.due_date = self.borrow_date + timedelta(
                days=self.LOAN_PERIOD_DAYS
            )

        # return_date is None while the book is still on loan
        if return_date and return_date.strip().lower() not in ("", "none"):
            self.return_date = date.fromisoformat(return_date)
        else:
            self.return_date = None

    def is_returned(self):
        """
        Check whether the book has been returned.

        Returns:
            bool: True if a return date has been recorded.
        """
        return self.return_date is not None

    def is_overdue(self):
        """
        Check whether the loan is overdue and not yet returned.

        Returns:
            bool: True if today is past the due date and the book
                  has not been returned.
        """
        if self.is_returned():
            return False
        return date.today() > self.due_date

    def mark_returned(self):
        """
        Record today as the return date for this loan.

        Returns:
            bool: True if marked successfully, False if already returned.
        """
        if not self.is_returned():
            self.return_date = date.today()
            return True
        return False

    def days_overdue(self):
        """
        Calculate how many days overdue the loan is.

        Returns:
            int: Number of overdue days, or 0 if not overdue.
        """
        if self.is_overdue():
            return (date.today() - self.due_date).days
        return 0

    def get_info(self):
        """
        Return a formatted string with the record's details.

        Returns:
            str: Human-readable summary of the borrow record.
        """
        status = "Returned" if self.is_returned() else (
            f"OVERDUE by {self.days_overdue()} day(s)"
            if self.is_overdue() else "On Loan"
        )
        returned_str = str(self.return_date) if self.return_date else "N/A"
        return (
            f"Record [{self.record_id}] | Member: {self.member_id} | "
            f"Book: {self.book_id} | Borrowed: {self.borrow_date} | "
            f"Due: {self.due_date} | Returned: {returned_str} | "
            f"Status: {status}"
        )

    def to_csv_row(self):
        """
        Serialise the record as a list for CSV writing.

        Returns:
            list: Fields in the order expected by the CSV file.
        """
        return [
            self.record_id,
            self.member_id,
            self.book_id,
            str(self.borrow_date),
            str(self.due_date),
            str(self.return_date) if self.return_date else ""
        ]

    @staticmethod
    def from_csv_row(row: list):
        """
        Create a BorrowRecord instance from a CSV row.

        Args:
            row (list): A list of string fields from the CSV file.

        Returns:
            BorrowRecord: A new BorrowRecord instance.
        """
        return BorrowRecord(
            record_id=row[0],
            member_id=row[1],
            book_id=row[2],
            borrow_date=row[3],
            due_date=row[4],
            return_date=row[5] if len(row) > 5 else None
        )
