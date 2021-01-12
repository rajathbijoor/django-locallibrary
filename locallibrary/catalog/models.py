from django.db import models
from django.urls import reverse #used to generate urls by reversing url patterns
import uuid #required for unique book instances/copies
from django.contrib.auth.models import User
from datetime import date


# Create your models here.
class Genre(models.Model):
    '''Model representing a book genre'''
    name = models.CharField(max_length=200, help_text="Enter a book Genre(ex: fiction/non-fiction")

    def __str__(self):
        '''String method for representing the model object'''
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=100, help_text="Langauge in which the book is published")

    def get_absolute_url(self):
        '''return the url to access a particular language instance'''
        return reverse('', args=[str(self.id)])

    def __str__(self):
        return self.name

class Book(models.Model):
    '''Model representing a book(but not a specific copy of a book'''
    title = models.CharField(max_length=200)

    #to declare author now, i have used foreignkey because book can have only one author whereas author may have
    #multiple books published in his name.also Author is declared as string rather than the object because it hasnt
    #been declared yet in file
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)

    summary = models.TextField(max_length=1000, help_text="Give a description about this book")
    isbn = models.CharField('ISBN', max_length=13, unique=True, help_text='refer mozilla')

    #ManyToManyField is used in genre filed because genre can contain many books and book can contain mant genres
    #Genre class is already defined so instead of string we can just mention genre field name in the parameter
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")

    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)
    #language = models.CharField(max_length=50, help_text="Language in which a book is published")

    def __str__(self):
        return self.title
        '''string for reprsenting a model object'''


    def display_genre(self):
        '''creating a string for the genre.this is required to run display_genre in admin.py'''
        return ', '.join(genre.name for genre in self.genre.all()[:3])


    def get_absolute_url(self):
        '''returns the url to access a detail record for this book'''
        return reverse('book-detail', args=[str(self.id)])

class BookInstance(models.Model):
    '''Model reprsenting a specific copy of a book(that is borrowed from llocal library)'''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=True, help_text="Unique ID of this book")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    LOAN_STATUS = (
        ('m', "Maintainance"),
        ('o', "On Loan"),
        ('a', "Available"),
        ('r', "Reserved")
    )
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)


    status=models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book Availability')

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False


    def __str__(self):
        return f'{self.id} ({self.book})'




class Author(models.Model):
    '''Model representing an author'''
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        '''return the url to access a particular author instance'''
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'

class UserProfileInfo(models.Model):

    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)

    portfolio_site = models.URLField(blank=True)
    profile_pic = models.ImageField(upload_to='profile_pic', blank=True)

    def __str__(self):
        return User.username






