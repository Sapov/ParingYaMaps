import datetime
from symtable import Class

from django.contrib.auth import get_user_model
from django.db import models

Users = get_user_model()


class Category(models.Model):
    name_category = models.CharField(max_length=255, verbose_name='Категория', unique=True)

class City(models.Model):
    name_city = models.CharField(max_length=255, verbose_name='Город', unique=True)

class Links(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    сity_name = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='Город')
    link = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    rate = models.CharField(max_length=255)
    estimation = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    site = models.CharField(max_length=255)
    mail = models.CharField(max_length=255)
    whatsapp = models.CharField(max_length=255)
    telegram = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Добавлено")  # date created
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Изменено")  # date update


class OrderStatus(models.Model):
    status = models.CharField(max_length=255, verbose_name='Статус ордера')


class Order(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name='Пользователь')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(verbose_name='Заказ оплачен', default=False)
    order_status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE, verbose_name='СТАТУС')
    price = models.IntegerField(verbose_name='Стоимость')

    def __str__(self):
        return self.id

    class Meta:
        verbose_name_plural = 'Заказы'
        verbose_name = 'Заказ'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Ордер')
    link  = models.ForeignKey(Links, on_delete=models.CASCADE, verbose_name='Ссылка')
