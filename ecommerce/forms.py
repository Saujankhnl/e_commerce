# ecommerce/forms.py
from django import forms
from .models import Category 
from .models import Product # Import from current app
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password1')


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category  # This should point to ecommerce.Category
        fields = ['name', 'slug', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter category name'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Will auto-generate from name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 4,
                'placeholder': 'Optional category description'
            }),
        }
  # Make sure you have a Product model

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'category', 'available', 'image']
