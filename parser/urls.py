from django.urls import path

from parser.views import index

urlpatterns = [

    path('', index, name='index')
]
