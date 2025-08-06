from bookshelf.models import Book
book_ = Book.objects.get(title="Nineteen Eighty-Four") # Retrieve the book by its updated title
book.delete()
print(Book.objects.all()) # Confirm deletion
