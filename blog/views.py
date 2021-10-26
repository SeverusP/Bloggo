from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import User, Post
from django.utils import timezone
from django.utils.timezone import now, datetime
import requests
from blog.forms import AuthenticationForm, UserRegisterForm, PostForm
from django.contrib import messages, auth
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count
from datetime import timedelta
from django.http import HttpResponse, HttpRequest

def posts(request):
    response = {}
    posts = Post.objects.filter().order_by('-datetime')
    for post in posts:
        response = {
            'datetime': post.datetime,
            'content' : post.content,
            'author' : f"{post.user.username}",
            'hash' : post.hash,
            'txId': post.txId,
        }
    return JsonResponse(response)


def welcome(request):
 return render (request, 'blog/Welcome.html', {})

def register_view(request):
    if request.POST:
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            username =form.cleaned_data.get('username')
            user.save()
            messages.success(request, f"New account created {username}! , Log in and publish your first post!")
            return redirect('/')
    else:
        form = UserRegisterForm()
    return render(request, 'blog/Register_form.html', {'form':form})


def login_view(request):
    context = {}
    form = AuthenticationForm(request.POST)
    if request.POST:
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
            if ip_address:
                ipaddress = ip_address.split(',')[-1].strip()
            else:
                ipaddress = request.META.get('REMOTE_ADDR')
            user = authenticate(username=username, password=password, ip=ipaddress)
            login(request, user)
            if request.user.ip != ipaddress:
                messages.success(request, "Attention! You've logged in with a different IP")
            request.user.ip = ipaddress
            request.user.save()
            return render(request, 'blog/Dashboard.html', context)
    return render(request, 'blog/Login_form.html', {'form': form})


@login_required
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/Post_list.html', {'posts':posts})


def logout_view(request):
    logout(request)
    return render(request, 'blog/Logout.html', {})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        writing = request.POST.get("content")
        if form.is_valid():
            if "hack" not in writing:
             post = form.save(commit=False)
             post.user = request.user
             post.published_date = timezone.now()
             post.save()
             return redirect('/login/post_list/')
            else:
                messages.success(request, "You cannot include the word HACK in your post!!")
                return render(request, 'blog/Change_post.html')

    else:
        form = PostForm()
    return render(request, 'blog/Post_new.html', {'form': form})


@user_passes_test(lambda user: user.is_superuser)
def num_post(request):
    user_posts = User.objects.annotate(total_posts = Count('post'))
    return render(request, 'blog/Users_activity.html', {'user_posts': user_posts})

def user_from_id(request, id):
    user_id = id
    user = User.objects.get(id=user_id)
    return render(request, 'blog/User_id.html', {'user_id':user_id, 'user':user})


def last_hour_posts(request):
    answer = {}
    dt = now()
    lhp_posts = Post.objects.filter(published_date__range=(dt-timedelta(hours=1),dt))
    for post in lhp_posts:
        answer = {
            'datetime': post.datetime,
            'content' : post.content,
            'author' : f"{post.user.username} ",
        }
    return JsonResponse(answer)


def string_in_posts(request, string):
            word = string
            number_posts = Post.objects.filter(content__contains=word).count()
            return render(request, 'blog/Number_posts.html', {'number_posts': number_posts, 'word' : word})