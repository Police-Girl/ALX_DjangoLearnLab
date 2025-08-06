from django.contrib import admin
from .models import Book #Imports the Book model

# Register your models here.
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
	# This list will display the specified fields in the list view
	list_display = ('title', 'author', 'publication_year')

	# This creates a filter sidebar on the right side of the list view
	list_filter = ('publication_year', 'author')

	# This adds a search box that searches the specified fields
	search_fields = ('title', 'author__name')
