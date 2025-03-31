from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from parser.forms import IndexForm
from .models import Order, Users, Links
from .tasks import run_parser


@login_required
def index(request):
    if request.POST:
        form = IndexForm(request.POST)
        if form.is_valid():
            qd = form.cleaned_data
            print(request.POST)
            сity_name = qd['сity_name']
            category = qd['category']
            # запускаем задачу в Celery
            user = Users.objects.get(username=request.user)
            order_id = Order.objects.create(user=user)
            print(order_id, type(order_id), order_id.id)
            run_parser.delay(category, сity_name, order_id.id)

            print('CLEAN DATA', qd['category'], type(qd['сity_name']))

            orders = Order.objects.filter(user=request.user)

            return render(request, "parser/order.html", {"orders": orders})

    else:
        form = IndexForm()
        return render(request, "parser/index.html", {"form": form})


def show_item(request, pk: int):
    li = Links.objects.filter(order_id=pk)
    return render(request, template_name='parser/item.html', context={'li': li})
