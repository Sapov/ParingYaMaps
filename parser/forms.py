from django import forms

from parser.models import Order, Links


class IndexForm(forms.Form):
        сity_name = forms.CharField(max_length=100, help_text='Город')
        category = forms.CharField(max_length=100, help_text='Категория')

