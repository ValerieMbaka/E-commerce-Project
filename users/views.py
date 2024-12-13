from django.shortcuts import render, redirect, get_object_or_404
from .models import FirebaseUser
from firebase_admin.exceptions import FirebaseError
from django.contrib import messages
from firebase_admin import auth
import firebase_admin
from firebase_admin import credentials
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from PIL import Image
from django.http import JsonResponse
import json

# Initialize Firebase Admin SDK
cred = credentials.Certificate(
                'C:/Users/user/OneDrive/Documents/Firebase/web-development-fe6af-firebase-adminsdk-chwhp-bea71374ea.json')
firebase_admin.initialize_app(cred)

# Create your views here.
def save_token(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                token = data.get('token')
                
                # Store the Firebase token in the session
                request.session['firebase_token'] = token
                
                return JsonResponse({'message': 'Token saved successfully'})


def signup_view(request):
        if request.method == 'POST':
                full_name = request.POST.get('full_name')
                email = request.POST.get('email')
                role = request.POST.get('role')
                password = request.POST.get('password')
                password_confirmation = request.POST.get('password_confirmation')
                
                # Validate form inputs
                if not all([full_name, email, role, password, password_confirmation]):
                        messages.error(request, "All fields are required.")
                        return redirect('users:signup')
                
                if password != password_confirmation:
                        messages.error(request, "Passwords do not match.")
                        return redirect('users:signup')
                
                # Check if the user already exists in Firebase
                try:
                        auth.get_user_by_email(email)
                        messages.error(request, "This email is already registered.")
                        return redirect('users:signup')
                except auth.UserNotFoundError:
                        pass  # User does not exist, proceed
                
                # Create the Firebase user
                try:
                        user = auth.create_user(
                                email=email,
                                password=password,
                                display_name=full_name
                        )
                except FirebaseError as e:
                        messages.error(request, f"Error creating user: {str(e)}")
                        return redirect('users:signup')
                
                # Save user in FirebaseUser model
                try:
                        FirebaseUser.objects.create(
                                uid=user.uid,
                                full_name=full_name,
                                email=email,
                                role=role
                        )
                except Exception as e:
                        auth.delete_user(user.uid)
                        messages.error(request, f"Error saving user: {e}")
                        return redirect('users:signup')
                
                # Success message
                messages.success(request, "Account created successfully!")
                # Redirect based on role
                if role == 'buyer':
                        return redirect('products:view_products')  # Redirect buyer to the products page
                else:
                        return redirect('products:upload_product')
        
        return render(request, 'users/signup.html')


def login_view(request):
        if request.method == 'POST':
                email = request.POST['email']
                password = request.POST['password']
                
                try:
                        user = auth.get_user_by_email(email)
                        # Simulate verification (Firebase Admin SDK doesn't handle passwords directly)
                        if verify_firebase_password(email, password):  # Custom helper function (mock)
                                request.session['firebase_uid'] = user.uid
                                messages.success(request, "Login successful.")
                                # Retrieve user's role from FirebaseUser model
                                try:
                                        firebase_user = FirebaseUser.objects.get(uid=user.uid)
                                        role = firebase_user.role
                                        
                                        # Redirect based on role
                                        if role == 'buyer':
                                                return redirect(
                                                        'products:view_products')  # Redirect buyer to products page
                                        else:
                                                return redirect(
                                                        'products:upload_product')  # Redirect seller to product upload page
                                
                                except FirebaseUser.DoesNotExist:
                                        messages.error(request, "User role not found.")
                                        return redirect('users:login')
                        
                        else:
                                messages.error(request, "Invalid credentials.")
                                return render(request, 'users/login.html')
                except Exception as e:
                        messages.error(request, f"Login failed: {e}")
                        return redirect('users:login')
        
        return render(request, 'users/login.html')


def verify_firebase_password(email, password):
        # Use Firebase client-side SDK for real verification (mocking here for backend demo)
        return password == password  # Replace with actual verification in production


@login_required
def buyer_dashboard_view(request):
        # Check if the user is logged in
        user_uid = request.session.get('firebase_uid')
        if user_uid is None:
                messages.error(request, "Session expired or user not logged in.")
                return redirect('users:login')
        
        try:
                firebase_user = FirebaseUser.objects.get(uid=user_uid)
                return render(request, 'users/buyer_dashboard.html', {'firebase_user': firebase_user})
        
        except FirebaseUser.DoesNotExist:
                messages.error(request, "User not found.")
                return redirect('users:login')


def logout_view(request):
        # Clear the session to log out the user
        try:
                del request.session['firebase_token']
        except KeyError:
                pass  # If the token doesn't exist, it's already logged out
        
        # Optionally, you can also log the user out from Firebase client-side using Firebase SDK
        
        return redirect('app1:index')  # Redirect to home or login page

@login_required
def delete_account_view(request):
        if request.method == "POST":
                try:
                        # Get the user from the FirebaseUser model
                        firebase_user = get_object_or_404(FirebaseUser, uid=request.session.get('firebase_uid'))
                        
                        # Delete the user from Firebase Authentication
                        auth.delete_user(firebase_user.uid)
                        
                        # Delete the user from the local model
                        firebase_user.delete()
                        
                        # Clear the session
                        request.session.flush()
                        
                        messages.success(request, "Your account has been permanently deleted.")
                        return redirect('app1:index')
                except Exception as e:
                        messages.error(request, f"Error deleting account: {e}")
                        return redirect('users:buyer_dashboard')
        return redirect('users:buyer_dashboard')


@login_required
def edit_details_view(request):
        if request.method == "POST":
                full_name = request.POST.get('full_name')
                email = request.POST.get('email')
                password = request.POST.get('password')
                
                try:
                        firebase_user = get_object_or_404(FirebaseUser, uid=request.session.get('firebase_uid'))
                        
                        # Update Firebase Authentication details
                        updated_fields = {}
                        if full_name:
                                updated_fields['display_name'] = full_name
                                firebase_user.full_name = full_name
                        if email:
                                updated_fields['email'] = email
                                firebase_user.email = email
                        if password:
                                updated_fields['password'] = password
                        
                        auth.update_user(firebase_user.uid, **updated_fields)
                        
                        # Save updates in the local database
                        firebase_user.save()
                        
                        messages.success(request, "Your details have been updated successfully.")
                except Exception as e:
                        messages.error(request, f"Error updating details: {e}")
                
                return redirect('users:buyer_dashboard')
        return redirect('users:buyer_dashboard')
