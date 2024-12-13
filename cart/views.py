from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import Product
from .models import CartItem


# Create your views here.
@login_required
def add_cart_item(request, product_id):
        if request.method == 'POST':
                product = get_object_or_404(Product, id=product_id)
                quantity = int(request.POST.get('quantity', 1))
                
                # Check if the item is already in the cart
                cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
                if created:
                        cart_item.quantity = quantity
                else:
                        cart_item.quantity += quantity
                
                cart_item.save()
                messages.success(request, f"{product.product_name} has been added to your cart.")
                return redirect('cart:cart')  # Update this to the correct view name for your cart page
        return redirect('products:products')
