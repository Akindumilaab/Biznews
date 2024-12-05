from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import profile


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text="Optional")
    last_name = forms.CharField(max_length=30, required=False, help_text="Optional")
    email = forms.EmailField(max_length=254, help_text='Enter a valid email address')

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        ]

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
        ]


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = profile
        fields = [
            'profile_picture',
            'address',
            'phone_number',
            'date_of_birth',
            'bio',
            'gender'
        ]

        widgets = {
            'date_of_birth': forms.NumberInput(attrs={'type':'date'}),
        }

class AdminProfileForm(forms.ModelForm):
    class Meta:
        model = profile
        fields = [
            'profile_picture',
            'address',
            'phone_number',
            'date_of_birth',
            'bio',
            'gender',
            'role'
        ]

        widgets = {
            'date_of_birth': forms.NumberInput(attrs={'type':'date'}),
        }