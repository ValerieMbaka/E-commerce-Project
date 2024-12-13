from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
        path('upload-product/', views.upload_product, name='upload_product'),
        path('view-products/', views.view_products, name='view_products'),
        path('product/<int:product_id>/', views.product_details, name='product_details'),
        path('update/<id>/', views.update_product, name='update'),
        path('delete/<id>/', views.delete_product, name='delete'),

]