from django.shortcuts import render, get_object_or_404,redirect
from django.views import generic
from django.http import HttpResponseRedirect
import datetime
from catalog.models import Book, Author, BookInstance, Genre
from catalog.forms import RenewBookForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse


def index(request):


    # Generate counts of main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # the all() is implied by default
    num_authors = Author.objects.count()

    #num_genres = Genre.objects.all().count()
    book_contains_x = Book.objects.filter(title__icontains='harry').count()

    query = request.GET.get('bookname',False)
    result = Book.objects.filter(title__icontains=query)

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'book_contains_x' : book_contains_x,
        'query' : query,
        'result': result,

    }

    return render(request, 'index.html', context=context)



class BookCreate(LoginRequiredMixin, CreateView):
    model = Book
    fields = '__all__'
    

class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')


class BookUpdate(UpdateView):
    model = Book
    fields = ['title','author','summary','isbn','genre']


class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'
    initial = {'date_of_death': '05/01/2018'}


class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')

class GenreCreate(CreateView):
	model = Genre
	fields = '__all__'


class BookListView(generic.ListView):
    model = Book
    
        

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author

class AuthorDetailView(generic.DetailView):

    model = Author



class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):

    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class LoanedBooksAllListView(PermissionRequiredMixin, generic.ListView):
    #Generic class based view listing all books on loan. Only visible to users with can_mark_returned permission.
    model = BookInstance
    permission_required = 'catalog.can_mark_returned'
    template_name = 'catalog/bookinstance_list_borrowed_all.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # if it is post request process the data
    if request.method == "POST":

        # create a form instance and load it with data from the request binding
        form = RenewBookForm(request.POST)

        # if the form contains valid data

        if form.is_valid():
            # here we write to the due-back field in the model with the new renewal date
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            return HttpResponseRedirect(reverse('all-borrowed'))
    # if it is get request set the initial value to 3 weeks
    else:
        if request.method == "GET":
            proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
            form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }
    return render(request, 'catalog/book_renew_librarian.html', context)




