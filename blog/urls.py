from django.conf.urls import url, include
from django.contrib import admin
from .views import login_view, register_view, logout_view
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns=[
    path('',views.welcome, name='welcome'),
    path('register/',views.register_view, name='register'),
    path('login/',views.login_view, name='login'),
    path('login/post_list/', views.post_list, name='post_list'),
    path('login/logout', views.logout_view, name='logout'),
    path('login/Post_new/', views.post_new, name='Post_new'),
    path('login/users_activity', views.num_post, name='Users_activity'),
    path('user/[<str:id>]', views.user_from_id, name='user_from_id'),
    path('lhp/', views.last_hour_posts),
    path('search/<str:string>', views.string_in_posts),
]