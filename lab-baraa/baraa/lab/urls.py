from django.urls import path
from . import views

urlpatterns = [
    path('product/<int:id>', views.product_list, name="product"),
    path('add_product', views.product_page, name="addProduct"),
    path('home', views.category_list, name="home"),
    path('sub/<int:id>', views.sub_category_list, name="sub"),
    path('product/notfound', views.not_found, name="notfound"),
    path('product/error', views.error, name="error"),
    path('sub/<int:id>/products', views.products, name="products"),
    path('edit_price', views.edit_price, name="editPrice"),
    path('products/<str:query>', views.products_search, name='search'),


]
