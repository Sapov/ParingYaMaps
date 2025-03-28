from django.shortcuts import render

from parser.forms import IndexForm
from .tasks import run_parser


def index(request):
    if request.POST:
        form = IndexForm(request.POST)
        if form.is_valid():
            qd = form.cleaned_data
            print(request.user)
            print(request.POST)
            сity_name = qd['сity_name']
            category = qd['category']
            #запускаем задачу в Celery
            run_parser.delay(category, сity_name)

            print('CLEAN DATA', qd['category'], type(qd['сity_name']))

            return render(request, "parser/order.html", {"form": form})

    else:
        form = IndexForm()
        return render(request, "parser/index.html", {"form": form})
