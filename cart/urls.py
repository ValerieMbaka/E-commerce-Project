from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
        path('add/<int:product_id>/', views.add_cart_item, name='add_to_cart'),
]