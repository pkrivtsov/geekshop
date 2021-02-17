from django.shortcuts import render
from django.core.paginator import Paginator
# from django.core.paginator import EmptyPage, PageNotAnInteger

from mainapp.models import Product, ProductCategory
import datetime


# Create your views here.

def index(request):
    return render(request, 'mainapp/index.html')


# def products(request, category_id=None):
#     products = Product.objects.filter(category_id=category_id) if category_id else Product.objects.all()
#     context = {
#         'title': datetime.datetime.now(),
#         'categories': ProductCategory.objects.all(),
#         'products': products,
#     }
#     return render(request, 'mainapp/products.html', context)

def products(request, category_id=None, page=1):
    if category_id:
        products = Product.objects.filter(category_id=category_id).order_by('-price')
    else:
        products = Product.objects.all().order_by('-price')
    per_page = 2
    paginator = Paginator(products, per_page)
    products_paginator = paginator.page(page)
    context = {'title': datetime.datetime.now(), 'categories': ProductCategory.objects.all(),
               'products': products_paginator}
    return render(request, 'mainapp/products.html', context)
    # try:
    #     products_paginator = paginator.page(page)
    # except PageNotAnInteger:
    #     products_paginator = paginator.page(1)
    # except EmptyPage:
    #     products_paginator = paginator.page(paginator.num_pages)
