# Gisma City Library Management System

A command-line Python application for managing a library's books, members, and borrowing records. Built as the primary project for **B100 Introduction to Computer Programming with Python** at Gisma University of Applied Sciences.

---

## Project Purpose

This system allows library staff to:
- Manage a catalogue of books (add, search, list)
- Register and manage library members
- Process book borrowing and returns
- Track overdue loans
- View a member's full loan history

All data is persisted to CSV files so it survives between sessions.

---

## Installation

**Requirements:** Python 3.8 or higher (no external libraries required — uses only the Python standard library).

1. Clone the repository:
   ```bash
   git clone https://github.com/siya2020-cyber/library-management-system-LMS
   cd library-management-system-LMS
   ```

2. No additional packages need to be installed.

---

## Running the Application

From inside the project folder, run:

```bash
python main.py
```

The program will:
1. Load any previously saved data from the `data/` folder.
2. Populate sample books and members if no data exists yet.
3. Display the interactive main menu.

---

## Example Usage

```
Welcome to the Gisma City Library Management System!

=======================================================
  Gisma City Library - Main Menu
=======================================================
  1. Add a new book
  2. Search books
  3. List all books
  4. Register a new member
  5. List all members
  6. Borrow a book
  7. Return a book
  8. View overdue loans
  9. View member loan history
  0. Exit
-------------------------------------------------------
  Enter your choice: 6

  Member ID: M001
  Book ID: B003
  '1984' borrowed by Alice Johnson. Due: 2026-04-19
```

---

## Key Features

- **Book Management** – Add books with ID, title, author, genre, year, and copy count. Search by any field.
- **Member Registration** – Register members and enforce a 3-book borrow limit.
- **Borrowing & Returns** – Full transaction tracking with automatic due dates (14-day loan period).
- **Overdue Detection** – Instantly lists all currently overdue loans.
- **Loan History** – View the complete borrowing history for any member.
- **Data Persistence** – All data saved automatically to `data/books.csv`, `data/members.csv`, and `data/records.csv`.
- **Error Handling** – Clear error messages for invalid IDs, unavailable books, and exceeded borrow limits.

---

## Project File Structure

```
library-management-system/
│
├── main.py            # Entry point; menu-driven interface
├── library.py         # Library class; core logic and file I/O
├── book.py            # Book class
├── member.py          # Member class
├── borrow_record.py   # BorrowRecord class
│
└── data/
    ├── books.csv      # Persisted book data
    ├── members.csv    # Persisted member data
    └── records.csv    # Persisted borrow records
```

---

## Module Overview

| File | Description |
|---|---|
| `book.py` | `Book` class — attributes and methods for a single book |
| `member.py` | `Member` class — member data and borrow limit enforcement |
| `borrow_record.py` | `BorrowRecord` class — tracks each loan transaction |
| `library.py` | `Library` class — central controller, file I/O, business logic |
| `main.py` | Entry point with interactive CLI menu |

---

## Academic Integrity

This project was designed and implemented independently as part of the B100 module assessment. All code is original work by me.
