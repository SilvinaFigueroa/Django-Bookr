from django.db.models import Avg, Q
from django.db.models.functions import Round
from django.shortcuts import render, get_object_or_404

from .forms import SearchForm
from .models import *
from .utils import average_rating


def index(request):
    return render(request, "base.html")


def book_search(request):
    search_input = request.GET.get("search", "")
    # SearchForm instance with GET request
    form = SearchForm(request.GET)
    # list to add the search results
    search_results = []

    # validate the form
    if form.is_valid() and form.cleaned_data["search"]:
        # get data from field set in form.py
        search = form.cleaned_data["search"]
        search_in = form.cleaned_data.get("search_in")

        if search_in == "title":
            search_results = Book.objects.filter(title__icontains=search)

        else:
            # Using a Q object to combine conditions and retrieve contributors from DB

            if search_in == "title":
                search_results = Book.objects.filter(title__icontains=search)
            else:
                search_results = Book.objects.filter(
                    Q(contributors__first_names__icontains=search) |
                    Q(contributors__last_names__icontains=search)
                )

    return render(request, "reviews/book-search.html",
                  {'form': form, 'search_input': search_input, 'search_results': search_results})


def book_list(request):
    books = Book.objects.all()
    book_list = []

    for book in books:
        reviews = book.review_set.all()

        if reviews:
            book_rating = average_rating([review.rating for review in reviews])
            number_of_reviews = len(reviews)
        else:
            book_rating = None
            number_of_reviews = 0

        book_list.append({'book': book, \
                          'book_rating': book_rating, \
                          'number_of_reviews': number_of_reviews})
    context = {
        'book_list': book_list
    }
    # request - URL - return for displaying on template
    return render(request, 'reviews/books_list.html', context)


def book_details(request, id):
    book = get_object_or_404(Book, id=id)
    reviews = book.review_set.all()
    review_list = []

    for element in reviews:
        content = element.content
        rating = element.rating
        date_created = element.date_created
        date_edited = element.date_edited
        creator = element.creator

        review_list.append({
            "content": content,
            "rating": rating,
            "date_created": date_created,
            "date_edited": date_edited,
            "creator": creator})

    book_rating = reviews.aggregate(avg_rating=Round(Avg('rating'), 2))['avg_rating']

    context = {"book": book, "book_rating": book_rating, "review_list": review_list}

    return render(request, 'reviews/book_details.html', context)
