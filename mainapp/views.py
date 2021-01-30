from django.shortcuts import render
import json
import datetime

# Create your views here.

def index(request):
    return render(request, 'mainapp/index.html')

def products(request):
    with open('mainapp/fixtures/products.json', 'r', encoding='utf-8') as fh:
        context = {
            'title': datetime.datetime.now(),
            'products': json.load(fh)
        }
    return render(request, 'mainapp/products.html', context)

