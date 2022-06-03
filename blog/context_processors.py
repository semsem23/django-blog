from django.shortcuts import render
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Category, Post
from django.conf import settings


def categories(request):
    objects = Category.objects.order_by('name')
    return {'categories': objects}