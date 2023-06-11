from PIL import Image
from django.db.models import Avg, Q
from django.db.models.functions import Round
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone

from .forms import SearchForm, PublisherForm, ReviewForm, BookMediaForm
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


# def book_details(request, id):
#     book = get_object_or_404(Book, id=id)
#     reviews = book.review_set.all()
#     review_list = []
#
#     for element in reviews:
#         content = element.content
#         rating = element.rating
#         date_created = element.date_created
#         date_edited = element.date_edited
#         creator = element.creator
#
#         review_list.append({
#             "content": content,
#             "rating": rating,
#             "date_created": date_created,
#             "date_edited": date_edited,
#             "creator": creator})
#
#     book_rating = reviews.aggregate(avg_rating=Round(Avg('rating'), 2))['avg_rating']
#     context = {"book": book, "book_rating": book_rating, "review_list": review_list}
#
#     return render(request, 'reviews/book_details.html', context)

def book_details(request, pk):
    book = get_object_or_404(Book, pk=pk)
    reviews = book.review_set.all()
    if reviews:
        book_rating = average_rating([review.rating for review in reviews])
        context = {
            "book": book,
            "book_rating": book_rating,
            "reviews": reviews
        }
    else:
        context = {
            "book": book,
            "book_rating": None,
            "reviews": None
        }
    return render(request, 'reviews/book_details.html', context)


def publisher_edit(request, pk=None):
    # validating is we are editing an existing publisher record or creating a new one
    if pk is not None:
        publisher = get_object_or_404(Publisher, pk=pk)
    else:
        publisher = None

    if request.method == "POST":
        form = PublisherForm(request.POST, instance=publisher)

        if form.is_valid():
            updated_publisher = form.save()
            # register a different success message depending on whether the Publisher instance was created or updated.
            if publisher is None:
                messages.success(request, "Publisher \"{}\" was created.".format(updated_publisher))
            else:
                messages.success(request, "Publisher \"{}\" was updated.".format(updated_publisher))

            return redirect("publisher_edit", updated_publisher.pk)

    else:
        # form fields are initialized with the data from the publisher object.
        form = PublisherForm(instance=publisher)

    return render(request, "reviews/instance-form.html",
                  {"instance": publisher, "model_type": Publisher, "form": form})


def review_edit(request, book_pk, review_pk=None):
    # get book object
    book = get_object_or_404(Book, pk=book_pk)

    # validation for reviews (updating an existent review or creating a new one)
    if review_pk is not None:
        review = get_object_or_404(Review, book_id=book_pk, pk=review_pk)
    else:
        review = None

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)

        if form.is_valid():
            updated_review = form.save(False)
            updated_review.book = book

            if review is None:
                messages.success(request, "Review for book \"{}\" created successfully.".format(book.title))

            else:
                # Updating date_edited for an edited review
                updated_review.date_edited = timezone.now()
                messages.success(request, "Review for book \"{}\" updated successfully.".format(book.title))

            # save updated_review manually since we passed the argument False in line 138
            updated_review.save()
            return redirect("book_details", book.pk)

    else:
        form = ReviewForm(instance=review)

    return render(request, "reviews/instance-form.html",
                  {"instance": review, "model_type": "Review", "form": form,
                   "related_model_type": "Book", "related_instance": book})


def book_media(request, pk):
    # get the book with the pk
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        form = BookMediaForm(request.POST, request.FILES, instance=book)

        if form.is_valid():
            # save set to "false" to allow us first to resize the image and then save it manually
            book = form.save(False)

            cover_file = form.cleaned_data.get('cover')
            if cover_file:
                image = Image.open(cover_file.file)
                image.thumbnail((300, 300))

                # save the resized image directly to the book.cover field
                book.cover.save(cover_file.name, cover_file)

            #  success message after upload image
            messages.success(request, "The image for book \"{}\" was updated successfully.".format(book))
            return redirect("book_details", book.pk)

    else:
        form = BookMediaForm(instance=book)

    return render(request, "reviews/instance-form.html",
                  {"instance": book, "form": form, "model_type": "Book", "is_file_upload": True})
