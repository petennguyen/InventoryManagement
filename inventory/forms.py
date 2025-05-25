from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Category, InventoryItems
class UserRegisterForm(UserCreationForm):

    email = forms.EmailField()

    class Meta:
        model = User
        fields = [ 'username', 'email', 'password1', 'password2']


class InventoryItemsForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), initial = 0)
    class Meta:
        model = InventoryItems
        fields = ['name', 'quantity', 'category']