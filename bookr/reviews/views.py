from django.shortcuts import render


# from django.http import HttpResponse
# This is what is used to create the response that goes back to the web browser

# def index(request):
#     name = request.GET.get("name") or "world"
#     return HttpResponse("Hello, {}!".format(name))
#
#     # http://127.0.0.1:8000/?name=Silvina

def index(request, name='User'):
    name = request.GET.get("name", name)
    context = {"name": name}
    return render(request, "review_base.html", context)


def search(request, book='My Book'):
    book = request.GET.get("book", book)
    context = {"book": book}
    return render(request, "search.html", context)


# from django.http import HttpResponse
# from .models import Book

## function using HTML inside it

# def welcome_view(request):
#     message = f'<html><h1>Welcome to Bookr!</h1> ' \
#               f'<p>{Book.objects.count()} books and counting!</p></html>'
#
#     return HttpResponse(message)

# function using a template to render the view
def welcome_view(request):
    return render(request, 'base.html')
