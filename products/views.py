from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Category, Product

# Create your views here.
def upload_product(request):
        # Capture user input
        if request.method == "POST":
                product_name = request.POST['product_name']
                product_price = request.POST['product_price']
                product_quantity = request.POST['product_quantity']
                product_description = request.POST['product_description']
                product_image = request.FILES['product_image']
                
                # Handle category selection
                product_category_id = request.POST['product_category']
                
                # If category exists or is selected
                try:
                        # Ensure the category ID is valid
                        if not product_category_id:
                                raise ValueError("No category selected.")
                        
                        # Try to fetch the existing category
                        product_category = Category.objects.get(id=product_category_id)
                        
                        # Save user input to the database
                        product = Product(
                                product_name=product_name,
                                product_price=product_price,
                                product_category=product_category,
                                product_quantity=product_quantity,
                                product_description=product_description,
                                product_image=product_image
                        )
                        product.save()
                        # Success message
                        messages.success(request, f"Product '{product.product_name}' uploaded successfully!")
                        
                        return redirect('app1:index')
                
                except Category.DoesNotExist:
                        messages.error(request, "Invalid category selected.")
                except Exception as e:
                        messages.error(request, f"An error occurred: {e}")
        
        # Fetch all categories
        categories = Category.objects.all()
        return render(request, 'products/upload_product.html', {"categories": categories})


def view_products(request):
        # Get all categories for the sidebar
        categories = Category.objects.all()
        
        # Get the selected category from the query parameter, if any
        selected_category_id = request.GET.get('category')
        
        # Filter products based on the selected category if applicable
        if selected_category_id:
                products = Product.objects.filter(product_category_id=selected_category_id)
        else:
                # If no category is selected, show all products
                products = Product.objects.all()
        
        # Implement pagination
        paginator = Paginator(products, 6)  # Show 6 products per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # Pass categories and products to the template
        return render(request, 'products/products.html', {
                'categories': categories,
                'page_obj': page_obj,
                'selected_category_id': selected_category_id,
        })


def product_details(request, product_id):
        product = Product.objects.get(id=product_id)
        return render(request, 'products/product_details.html', {'product': product})


# Function to update product details
def update_product(request, id):
        product = Product.objects.get(id=id)
        # Getting the new product values
        if request.method == "POST":
                product_name = request.POST['product_name']
                product_price = request.POST['product_price']
                product_category = request.POST['product_category']
                product_quantity = request.POST['product_quantity']
                product_description = request.POST['product_description']
                product_image = request.FILES['product_image']
                
                # Equating the new values to the existing product values
                product.product_name = product_name
                product.product_price = product_price
                product.product_category = product_category
                product.product_quantity = product_quantity
                product.product_description = product_description
                product.product_image = product_image
                
                # Save the new values to the database
                product.save()
                
                # Redirect to the view_products page
                return redirect('products:view_products')
        
        return render(request, 'products/update_product.html', {'product': product})


def delete_product(request, id):
        product = Product.objects.get(id=id)
        product.delete()
        return redirect('products:view_products')