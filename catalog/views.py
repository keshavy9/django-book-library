from django.shortcuts import render
from django.views import generic

from catalog.models import Book, Author, BookInstance, Genre


class BookListView(generic.ListView):
    model = Book


class BookDetailView(generic.ListView):
    model = Book


def index(request):


    # Generate counts of main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # the all() is implied by default
    num_authors = Author.objects.count()

    # challenges

    num_genres = Genre.objects.all().count()
    book_contains_x = Book.objects.filter(title__icontains='harry').count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'book_contains_x' : book_contains_x,
    }

    return render(request, 'index.html', context=context)




