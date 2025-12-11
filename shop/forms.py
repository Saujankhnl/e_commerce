from django import forms
from ecommerce.models import Category 

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "slug", "description"]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500',
                'placeholder': 'Enter category name'
            }),  # ← Added missing closing brace and comma
            'description': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500',
                'placeholder': 'Enter category description',
                'rows': 3
            }),
        }