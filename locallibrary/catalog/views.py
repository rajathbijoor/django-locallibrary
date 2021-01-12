from .models import Book, BookInstance, Author, Genre, Language
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

import datetime
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import RenewBookForm

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from django.urls import reverse
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required

from catalog.forms import UserForm, UserProfileInfoForm
# Create your views here.

class BookListView(generic.ListView):
    model = Book

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author

class AuthorDetailView(generic.DetailView):
    model = Author

def index(request):
    '''veiw function for homepage of site'''

    '''i) generate count of some of the main objects(books,copies)'''
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    '''ii) available books(status = 'a')'''
    book_status = BookInstance.objects.filter(status__exact='a').count()

    '''iii) no of authors.. note: all() will be implied by default if its not typed'''
    no_of_authors = Author.objects.count()

    no_of_genre_category = Genre.objects.all().count()

    num_of_languages = Language.objects.all().count()

    '''No of visits to this view as counted in session variable'''

    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1


    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'book_status': book_status,
        'no_of_authors': no_of_authors,
        'no_of_genre_category': no_of_genre_category,
        'num_visits': num_visits,
        'num_of_languages': num_of_languages,

    }


    '''render the HTML template index.html with the data in context variable'''
    return render(request, 'index.html', context=context)

   #creating view for on-loan details of particular user
class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
        '''generic class based view listings boooks on loan to current user'''
        model = BookInstance
        template_name = 'catalog/book_instance_list_borrowed_user.html'
        paginate_by = 3

        def get_queryset(self):
            return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


@login_required
#@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    '''view function for creating a specific book instance y librarian'''
    book_instance = get_object_or_404(BookInstance, pk=pk)

    #if this is a POST request then process the form data
    if request.method == 'POST':
        #create a form instance and populate it with data from the request(binding)
        form = RenewBookForm(request.POST)

        #check if the form is valid:
        if form.is_valid():
            #process the data in form.cleaned_data as required(here we just write it to model due_back field)

            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            #redirect to a new URL:
            return HttpResponseRedirect(reverse('books'))
    #If this is a GET create a default form
    else:
        proposed_renewal_date= datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }
    return render(request, 'catalog/book_renew_librarian.html', context)

class AuthorCreate(CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']


class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('Authors')

class BookCreate(CreateView):
    model = Book
    fields = ['title', 'author', 'genre', 'isbn', 'summary']

class BookUpdate(UpdateView):
    model = Book
    fields = ['title', 'author', 'genre', 'isbn', 'summary']

class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')

#creating view for on-loan details of all users
class LoanedBooksByAllUsersListview(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/book_instance_list_of_all_users_borrowed_visible_to_staffONLY.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')


def user_login(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('catalog:index'))

            else:
                return HttpResponse("Account not active")
        else:
            print("Some tried to login and failed")
            print("username: {} and password:{} is not valid".format(username, password))
            return HttpResponse("Incorrect credentails supplied")
    else:
        return render(request, 'registration/login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('catalog:user_login'))

@login_required
def special(request):
    return HttpResponse("You are logged in!!")

def register(request):
    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'basic_app/registration.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})

