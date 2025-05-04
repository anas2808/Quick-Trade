from django import forms
from Quick_Trade_Client.models import *
from Quick_Trade_admin.models import*

class Categories(forms.ModelForm):
    class Meta:
        model = main_categories
        fields = ['categories_name','image']

        widgets = {
            'categories_name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter category name',
                'id': 'sub-category-name'
            }),
            'image': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'category-image',
                'placeholder':'Enter font icon class',
            }),
        }
        
# class Sub_Categories(forms.ModelForm):
#     class Meta:
#         model = sub_categories
#         fields = ['main_categories','sub_categories_name','image']

#         widgets = {
#             'main_categories': forms.Select(attrs={
#                 'class': 'form-control',
#                 'id': 'main-category-select'  
#             }),
#             'sub_categories_name': forms.TextInput(attrs={
#                 'class': 'form-control', 
#                 'placeholder': 'Enter sub-category name',
#                 'id': 'sub-category-name'
#             }),
#             'image': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'id': 'category-image',
#                 'placeholder':'Enter font icon class',
#             }),
#         }
        
        
class EditProfile(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'phone', 'profile_picture', 'bio']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
