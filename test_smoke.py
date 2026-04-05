"""
test_smoke.py - Quick smoke test for the Library Management System.
Usage: python test_smoke.py
"""

import sys, os, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from book import Book
from member import Member
from library import Library

PASS = "\033[92mPASS\033[0m"
FAIL = "\033[91mFAIL\033[0m"
DATA_DIR = "test_tmp"
results = []

def test(desc, fn):
    try:
        fn()
        print(f"  {PASS}  {desc}")
        results.append(True)
    except Exception as e:
        print(f"  {FAIL}  {desc} — {e}")
        results.append(False)

def raises(fn):
    try:
        fn()
        raise AssertionError("expected ValueError")
    except ValueError:
        pass

def setup():
    shutil.rmtree(DATA_DIR, ignore_errors=True)
    lib = Library("Test", data_dir=DATA_DIR)
    lib.add_book(Book("B001", "1984", "Orwell", "Fiction", 1949, 1))
    lib.add_book(Book("B002", "Clean Code", "Martin", "Programming", 2008, 1))
    lib.add_book(Book("B003", "Sapiens", "Harari", "History", 2011, 1))
    lib.register_member(Member("M001", "Alice", "a@t.com", "555"))
    lib.register_member(Member("M002", "Bob",   "b@t.com", "556"))
    return lib

print("\n=== Library Smoke Tests ===\n")

lib = setup()
test("Borrow a book",           lambda: lib.borrow_book("M001", "B001"))
test("Book copy decremented",   lambda: None if lib.books["B001"].available_copies == 0 else (_ for _ in ()).throw(AssertionError()))
test("Return a book",           lambda: lib.return_book("M001", "B001"))
test("Book copy restored",      lambda: None if lib.books["B001"].available_copies == 1 else (_ for _ in ()).throw(AssertionError()))
test("Search by author",        lambda: None if lib.search_books("orwell") else (_ for _ in ()).throw(AssertionError("no results")))
test("Duplicate book raises",   lambda: raises(lambda: lib.add_book(Book("B001", "x", "x", "x", 2000, 1))))
test("Borrow unknown book",     lambda: raises(lambda: lib.borrow_book("M001", "B999")))
test("Borrow limit enforced",   lambda: (lib.borrow_book("M001","B001"), lib.borrow_book("M001","B002"), lib.borrow_book("M001","B003"), raises(lambda: lib.borrow_book("M002","B001"))))
test("Data persists on reload", lambda: None if "B001" in Library("R", data_dir=DATA_DIR).books else (_ for _ in ()).throw(AssertionError()))

shutil.rmtree(DATA_DIR, ignore_errors=True)
print(f"\n  {sum(results)}/{len(results)} passed\n")
sys.exit(0 if all(results) else 1)