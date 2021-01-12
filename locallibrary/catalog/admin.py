from django.contrib import admin
from .models import Author, Genre, Book, BookInstance, Language, UserProfileInfo
# Register your models here.

#admin.site.register(Book)
#admin.site.register(BookInstance)
admin.site.register(Genre)
#admin.site.register(Author)
admin.site.register(Language)



#to change how a model is displayed in the admin interface

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    '''the fileds attribute usedhere lists just those fields that are to be displayed in the form
    fileds by defualt get displayed verticaly.it will display horizontally if you group them inside tuple'''

admin.site.register(Author, AuthorAdmin)

'''the above can also be written as @admin.register(Author)
                                    class AuthorAdmin(admin.ModelAdmin):
                                         pass'''




@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre', 'language')

    '''inlines=[BookInstanceInline] 
       the inline method helps us to add associated records of one or more model together at the sma etime
       inlines display in 2 format 1.tabularinline(horizontal layout) 2.stackedinline(vertical layout)'''


'''we can add sectionns to group relaated model information within detail form using fieldssets
in boookinstance we have information related to what the book is(i.e name,imprint,id) and its availablity(status,due_back)
we can add these into different sections by adding text in bold to our BookInstanceAdmin class'''
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')
    fieldsets = (
        (None, {
                 'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
                           'fields': ('status', 'due_back', 'borrower')
        }),
    )

'''cif admin classes are empty(ie if only pass is used) hence admin behaviour will be unchanged.'''

admin.site.register(UserProfileInfo)