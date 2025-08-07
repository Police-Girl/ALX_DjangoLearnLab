from django.db import models

class Author(models.Model):
	name = models.CharField(max_length = 100)  #Object's desctription
	def __str__(self): #any function within a class must take self within that argument
		return self.name  #calls the description...yet to know how it works..

class Book(models.Model):
	title = models.CharField(max_length = 100)
	author = models.ForeignKey(Author, on_delete=models.CASCADE) #we only use cascade when the parent exists, so you only use it in the child  class
	def __str__(self): #functionnn wacha kusahauuu
		return f" {self.title}, {self.author.name}" #its best used when returning formatted string to pick up both variables.

class Library(models.Model):
	name = models.CharField(max_length = 100)
	books = models.ManyToManyField(Book)
	def __str__(self):
		return f"{self.name} , {self.books.title}"

class Librarian(models.Model):
	name = models.CharField(max_length =100)
	library = models.OneToOneField(Library, on_delete=models.CASCADE)
	def __str__(self):
		return f"{self.name} ,{self.library.name}" 


# Create your models here.
