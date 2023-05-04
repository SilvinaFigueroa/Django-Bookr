
from django.shortcuts import render

# from django.http import HttpResponse
# This is what is used to create the response that goes back to the web browser

# def index(request):
#     name = request.GET.get("name") or "world"
#     return HttpResponse("Hello, {}!".format(name))
#
#     # http://127.0.0.1:8000/?name=Silvina

def index(request, name = 'User'):
    name = request.GET.get("name", name)
    context = {"name": name}
    return render(request, "base.html", context)

def search(request, book = 'My Book'):
    book = request.GET.get("book", book)
    context = {"book": book}
    return render(request, "search.html", context)