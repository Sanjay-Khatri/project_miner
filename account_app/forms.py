from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserForm(UserCreationForm):

    FirstName = forms.CharField(max_length=30,widget=forms.TextInput())
    LastName = forms.CharField(max_length=30,widget=forms.TextInput())




    class Meta():
        model = User
        fields = ('username', 'email')
        required = ('username', 'email')
        widgets = {
            'username': forms.TextInput(),
            'email': forms.TextInput(),
        }
