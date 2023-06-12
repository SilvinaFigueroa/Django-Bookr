from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer, ContributionSerializer, ContributorSerializer

# @api_view()
# def all_books(request):
#     # This view takes a query set containing all books and then serializes them using BookSerializer
#     books = Book.objects.all()
#     book_serializer = BookSerializer(books, many=True)
#     return Response(book_serializer.data)

from rest_framework import generics
from .models import Book, Contributor
from .serializers import BookSerializer

# class-based view, we do not have to write a function that directly handles the request and calls the serializer
class AllBooks(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class ContributorView(generics.ListAPIView):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer

