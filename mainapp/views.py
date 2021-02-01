from django.shortcuts import render
from mainapp.models import Product, ProductCategory
import datetime

# Create your views here.

def index(request):
    return render(request, 'mainapp/index.html')

def products(request, id=None):
    print(id)
    context = {
        'title': datetime.datetime.now(),
        'products': Product.objects.all(),
        'categories': ProductCategory.objects.all(),
    }
    return render(request, 'mainapp/products.html', context)

