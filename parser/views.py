from django.shortcuts import render

from parser.forms import IndexForm


def index(request):
    if request.POST:
        form = IndexForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            print(request.user)
            print(request.POST)

            return render(request, "parser/order.html", {"form": form})

    else:
        form = IndexForm()
        return render(request, "parser/index.html", {"form": form})

