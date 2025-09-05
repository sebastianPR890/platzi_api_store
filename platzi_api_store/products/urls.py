from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('show_product/', views.show_product, name='show_product'),
    path('add_product/', views.add_product, name='add_product'),
    path('add_product_page/', views.add_product_page, name='add_product_page'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('api/product/<int:product_id>/', views.get_product_detail, name='get_product_detail'),
    path('product/update/<int:product_id>/', views.product_update, name='product_update_page'),
    path('api/product/update/<int:product_id>/', views.update_product, name='update_product_api'),
]   