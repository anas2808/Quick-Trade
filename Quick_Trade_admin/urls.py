from django.urls import path,include
from .views import *
from . import views

urlpatterns = [
    path('admin_dash/',admin_dash,name='admin_dash'),
    path('edit_profile_view/', views.edit_profile_view, name='edit_profile_view'),
    path('login/',views.admin_login,name='admin-login'),

    
    #Category URLs
    path('categories_list/',category_list,name='Category_list'),
    path('create_category/',create_category,name='Create_category'),
    path('update_category/<int:pk>',update_category,name='Update_category'),
    path('delete_category/<int:pk>',delete_category,name='Delete_category'),
    
    # #Sub category URLs
    # path('sub_categories_list/',Sub_category_list,name='Sub_Category_list'),
    # path('create_sub_category/',create_Sub_category,name='Create_Sub_category'),
    # path('update_sub_category/<int:pk>',update_Sub_category,name='Update_Sub_category'),
    # path('delete_sub_category/<int:pk>',delete_Sub_category,name='Delete_Sub_category'),
    
    #User URLs
    path('user_list/',user_list,name='User_list'),
    
    #listings URLs
    path('listings/',listings,name='listings'),
    path('update-status/<int:product_id>/', views.update_ad_status, name='update_ad_status'),
    

]