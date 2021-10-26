from django import forms
from django.forms import ModelForm
from django.shortcuts import render, redirect
from django.contrib.auth import (authenticate, get_user_model, login, logout,)
from django.contrib.auth.models import User
from blog.models import Post
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

User = get_user_model()


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)


class AuthenticationForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            user = authenticate(username=username, password=password,)
            if not user:
                raise forms.ValidationError('Wrong username or password')
        return super(AuthenticationForm,self).clean(*args, **kwargs)

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title','content')