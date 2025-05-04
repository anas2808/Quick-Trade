from .views import register_view, login_view, logout_view
from django.urls import path,include
from .views import *
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/',views.profile,name='profile'),
    path('edit-profile/', views.edit_profile_view, name='edit_profile'),
    
    

    #product detail
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('sell/', views.sell, name='sell'),
    path('Delete-Listing/<int:product_id>/', views.Delete_listing, name='delete_listing'),
    path('Update-Listing/<int:product_id>/', views.Update_product, name='update_product'),
    path('product_list/',views.product_list,name='product_list'),
    path('User_listing/<str:username>/',views.user_listing,name='user_listing'),

    
    #path('search_by_category/',views.search_product_category,name='search_by_category'),
    
    
    #messages
    path('messages/', views.message_list, name='message_list'),
    path('messages/new/<str:receiver_id>/<int:product_id>/', views.send_message, name='send_message_product'),
    path('messages/new/<str:receiver_id>/', views.send_message, name='send_message'),
    path('messages/<int:message_id>/', views.message_detail, name='message_detail'),

        


    

]
