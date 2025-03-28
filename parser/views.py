from django.shortcuts import render

from parser.forms import IndexForm
from .core.maps import Parse

def index(request):
    if request.POST:
        form = IndexForm(request.POST)
        if form.is_valid():
            qd = form.cleaned_data
            print(request.user)
            print(request.POST)
            Parse(qd['сity_name'], qd['category']).run()
            print('CLEAN DATA', qd['category'], type(qd['сity_name']))

            return render(request, "parser/order.html", {"form": form})

    else:
        form = IndexForm()
        return render(request, "parser/index.html", {"form": form})
