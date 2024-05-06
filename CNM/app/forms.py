from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from .models import CustomUser, Profile, Posts

class UserLoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class UserSignupForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'email', 'phone', 'gender', 'facebook', 'image']
        widgets={
            'full_name': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'phone': forms.TextInput(attrs={'class':'form-control'}),
            'gender': forms.Select(attrs={'class':'form-control'}),
            'facebook': forms.URLInput(attrs={'class':'form-control'}),
            'image': forms.FileInput(attrs={'class':'form-control'}),
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ('description', 'title', 'price', 'address', 'available', 'image', 'images1', 'images2', 'images3', 'images4', 'images5', 'post_type')
        labels = {
            'title': '',
            'price': '',
            'address': '',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Post title'}),
            'price': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Price'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'post_type': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'images1': forms.FileInput(attrs={'class': 'form-control'}),
            'images2': forms.FileInput(attrs={'class': 'form-control'}),
            'images3': forms.FileInput(attrs={'class': 'form-control'}),
            'images4': forms.FileInput(attrs={'class': 'form-control'}),
            'images5': forms.FileInput(attrs={'class': 'form-control'}),
        }
