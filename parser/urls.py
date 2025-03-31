from django.urls import path

from .views import index, show_item

urlpatterns = [

    path('', index, name='index'),
    path('show_item/<int:pk>', show_item, name='show_item'),
]
