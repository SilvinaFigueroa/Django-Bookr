from django.db.models import Avg
from django.db.models.functions import Round
from django.shortcuts import render, get_object_or_404
from .models import *
from .utils import average_rating


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
