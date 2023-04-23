from django.shortcuts import render

from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

# TODO: Add other views for data retrieval, data display, Load more, and Value Count functionalities.

