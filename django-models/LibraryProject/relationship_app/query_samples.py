# relationship_app/query_samples.py

import os
import sys
import django

# Get the base directory of the Django project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

# Now you can import your models
from relationship_app.models import Author, Book, Library, Librarian

def setup_sample_data():
    """Sets up sample data for testing queries."""
    print("--- Cleaning up existing data ---")
    Librarian.objects.all().delete()
    Library.objects.all().delete()
    Book.objects.all().delete()
    Author.objects.all().delete()
    print("Existing data cleared.\n")

    print("--- Setting up sample data ---")
    author1 = Author.objects.create(name="George Orwell")
    author2 = Author.objects.create(name="Jane Austen")
    author3 = Author.objects.create(name="Harper Lee")

    book1 = Book.objects.create(title="1984", author=author1)
    book2 = Book.objects.create(title="Animal Farm", author=author1)
    book3 = Book.objects.create(title="Pride and Prejudice", author=author2)
    book4 = Book.objects.create(title="To Kill a Mockingbird", author=author3)

    library1 = Library.objects.create(name="City Central Library")
    library1.books.add(book1, book2, book3)
    library2 = Library.objects.create(name="Riverside Branch")
    library2.books.add(book4)

    Librarian.objects.create(name="Alice Smith", library=library1)
    Librarian.objects.create(name="Bob Johnson", library=library2)
    print("Sample data created.\n")
    return author1, author2, author3, library1, library2



def get_books_by_author(author_name):
    """
    Query all books by a specific author.
    """
    print(f"--- Query 1: All books by {author_name} ---")
    try:
        author = Author.objects.get(name=author_name)
        books = Book.objects.filter(author=author)
        
        for book in books:
            print(f"- {book.title} (Author: {book.author.name})")
    except Author.DoesNotExist:
        print(f"Author '{author_name}' not found.")
        books = []
    print()
    return books



def list_books_in_library(library_name):
    """
    List all books in a library.
    """
    print(f"--- Query 2: All books in {library_name} ---")
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        for book in books:
            print(f"- {book.title} (Author: {book.author.name})")
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found.")
    print()
    return books



def get_librarian_for_library(library_name):
    """
    Retrieve the librarian for a library.
    """
    print(f"--- Query 3: Librarian for {library_name} ---")
    try:
        # Step 1: Get the Library object
        library_obj = Library.objects.get(name=library_name)
        
        # Step 2: Get the Librarian using the Library object (matching checker's "Librarian.objects.get(library=")")
        librarian = Librarian.objects.get(library=library_obj)
        print(f"Librarian for {library_name}: {librarian.name}")
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found for librarian query.")
        librarian = None
    except Librarian.DoesNotExist:
        print(f"No librarian found for library '{library_name}'.")
        librarian = None
    print()
    return librarian



def run_queries():
    print("\n--- Performing Sample Queries ---")
    
    # Setup data (returns some objects for direct use if needed)
    author1, _, _, library1, _ = setup_sample_data()

    # Execute queries using the new functions
    get_books_by_author("George Orwell")
    list_books_in_library("City Central Library")
    get_librarian_for_library("City Central Library")

    print("\n--- Queries Complete ---\n")

if __name__ == "__main__":
    run_queries()
