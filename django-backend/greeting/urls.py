from django.urls import path
from .views import create_product, list_products,  login_view,get_product_detail,add_stock,remove_stock

urlpatterns = [
    path('login/', login_view, name='login'),
    path('create_product/', create_product, name='create_product'),
    path('list_products/', list_products, name='list_products'),
   
    path('products/<slug:product_id>/', get_product_detail, name='get_product_detail'),
    path('products/<uuid:product_id>/variants/<int:variant_id>/add_stock/', add_stock, name='add_stock'),

   
    path('products/<uuid:product_id>/subvariants/<int:subvariant_id>/add_stock/', add_stock, name='add_stock_subvariant'),
    path('products/<uuid:product_id>/variants/<int:variant_id>/remove_stock/', remove_stock, name='remove_stock_variant'), 
    path('products/<uuid:product_id>/subvariants/<int:subvariant_id>/remove_stock/', remove_stock, name='remove_stock_subvarientvariant'), 
]