from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import *



class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'first_name', 'last_name', 'phone', 'profile_picture', 'bio', 'password', 'confirm_password']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'password' :forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'})),
            'confirm_password': forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'})),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")
        return cleaned_data


class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput,label="Password")
    class Meta:
        model = CustomUser
        fields = ['username', 'password']
        widgets = {
            'username': forms.EmailInput(attrs={'class': 'form-control form-control-lg border-left-0'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control form-control-lg border-left-0'}),
            }
        



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [ 'main_category','name', 'description', 'price', 'condition', 'location','image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'condition': forms.Select(attrs={'class': 'form-select'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'main_category': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        
        
class ProductSearchForm(forms.Form):
    search = forms.CharField(required=False)
    category = forms.ModelChoiceField(
        queryset=main_categories.objects.all(),
        required=False,
        empty_label="All Categories"
    )
    sort_by = forms.ChoiceField(
        choices=[('newest', 'Newest'), ('price_low', 'Price (Low to High)'), ('price_high', 'Price (High to Low)')],
        required=False
    )
    sort_by = forms.ChoiceField(
        choices=[
            ('newest', 'Newest'),
            ('price_low', 'Price Low to High'),
            ('price_high', 'Price High to Low'),
        ],
        required=False
    )
    price_min = forms.DecimalField(required=False, min_value=0)
    price_max = forms.DecimalField(required=False, min_value=0)
    
    
    condition = forms.MultipleChoiceField(
        choices=Product.CONDITION_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Enter your message here...'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Message subject'})
        }
    
class EditProfileForm(forms.ModelForm):
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
