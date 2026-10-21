from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import *


class UserRegistrationForm(forms.ModelForm):
    profile_picture = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={"class": "form-control qt-register-control", "accept": "image/*"}),
    )
    terms_accepted = forms.BooleanField(
        label="I agree to the Terms of Service and Privacy Policy",
        required=True,
        error_messages={"required": "You must accept the Terms of Service and Privacy Policy to create an account."},
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            "class": "form-control qt-register-control",
            "placeholder": "Create a strong password",
            "autocomplete": "new-password",
        }),
    )
    confirm_password = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(attrs={
            "class": "form-control qt-register-control",
            "placeholder": "Enter your password again",
            "autocomplete": "new-password",
        }),
    )

    class Meta:
        model = CustomUser
        fields = [
            "username", "email", "first_name", "last_name", "phone",
            "profile_picture", "bio", "password", "confirm_password",
            "terms_accepted",
        ]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control qt-register-control", "placeholder": "Choose a username", "autocomplete": "username"}),
            "email": forms.EmailInput(attrs={"class": "form-control qt-register-control", "placeholder": "you@example.com", "autocomplete": "email"}),
            "first_name": forms.TextInput(attrs={"class": "form-control qt-register-control", "placeholder": "First name", "autocomplete": "given-name"}),
            "last_name": forms.TextInput(attrs={"class": "form-control qt-register-control", "placeholder": "Last name", "autocomplete": "family-name"}),
            "phone": forms.TextInput(attrs={"class": "form-control qt-register-control", "placeholder": "Phone number", "autocomplete": "tel", "inputmode": "tel", "maxlength": "15"}),
            "bio": forms.Textarea(attrs={"class": "form-control qt-register-control", "rows": 3, "placeholder": "Tell other members a little about yourself"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match")
        return cleaned_data


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            "class": "form-control form-control-lg",
            "placeholder": "Enter your email address",
            "autocomplete": "email",
            "autofocus": True,
        }),
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={
            "class": "form-control form-control-lg",
            "placeholder": "Enter your password",
            "autocomplete": "current-password",
        }),
    )

    class Meta:
        model = CustomUser
        fields = ["username", "password"]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["main_category", "name", "description", "price", "condition", "location", "image"]
        widgets = {
            "main_category": forms.Select(attrs={"class": "form-select", "aria-label": "Product category"}),
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. iPhone 13, study table"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 5, "placeholder": "Describe the item's condition, features, and any important details"}),
            "price": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Enter price in ₹", "min": "0", "step": "0.01", "inputmode": "decimal"}),
            "condition": forms.Select(attrs={"class": "form-select"}),
            "location": forms.TextInput(attrs={"class": "form-control", "placeholder": "City or area, e.g. Ahmedabad"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control", "accept": "image/*"}),
        }


class ProductSearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        widget=forms.SearchInput(attrs={"class": "form-control", "placeholder": "Search products...", "aria-label": "Search products"}),
    )
    category = forms.ModelChoiceField(
        queryset=main_categories.objects.all(),
        required=False,
        empty_label="All Categories",
        widget=forms.Select(attrs={"class": "form-select", "aria-label": "Filter by category"}),
    )
    sort_by = forms.ChoiceField(
        choices=[
            ("newest", "Newest"),
            ("price_low", "Price Low to High"),
            ("price_high", "Price High to Low"),
        ],
        required=False,
        widget=forms.Select(attrs={"class": "form-select", "aria-label": "Sort products"}),
    )
    price_min = forms.DecimalField(
        required=False, min_value=0,
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "Minimum ₹", "min": "0", "step": "0.01"}),
    )
    price_max = forms.DecimalField(
        required=False, min_value=0,
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "Maximum ₹", "min": "0", "step": "0.01"}),
    )
    condition = forms.MultipleChoiceField(
        choices=Product.CONDITION_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={"class": "form-check-input"}),
    )


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["subject", "content"]
        widgets = {
            "subject": forms.TextInput(attrs={"class": "form-control", "placeholder": "Message subject"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 5, "placeholder": "Write your message here..."}),
        }


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["username", "first_name", "last_name", "phone", "profile_picture", "bio"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control", "placeholder": "Choose a username", "autocomplete": "username"}),
            "first_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "First name", "autocomplete": "given-name"}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Last name", "autocomplete": "family-name"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Phone number", "autocomplete": "tel", "inputmode": "tel"}),
            "profile_picture": forms.ClearableFileInput(attrs={"class": "form-control", "accept": "image/*"}),
            "bio": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Write a short profile bio"}),
        }
