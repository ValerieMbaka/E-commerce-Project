from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
        path('save_token/', views.save_token, name='save_token'),
        path('signup/', views.signup_view, name='signup'),
        path('login/', views.login_view, name='login'),
        path('logout/', views.logout_view, name='logout'),
        path('buyer-dashboard/', views.buyer_dashboard_view, name='buyer_dashboard'),
        path('delete-account/', views.delete_account_view, name='delete_account'),
        path('edit-details/', views.edit_details_view, name='edit_details'),
        # path('upload-profile-picture/', views.upload_profile_picture, name='upload_profile_picture'),
]