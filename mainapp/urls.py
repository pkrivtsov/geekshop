from django.urls import path

from mainapp.views import products

app_name = 'mainapp'

urlpatterns = [
    path('', products, name='index'),
    path('<int:category_id>/', products, name='product'), # /products/1/
    path('page/<int:page>/', products, name='page'), # /page/1/
]
