from django.urls import path
from .index_views import index

urlpatterns = [
    path('', index, name='index'),
]