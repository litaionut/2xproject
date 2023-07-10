"""
URL configuration for twoxproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . views import (
    login_view, 
    register_view,
    profile,
    step_list_recent,
    UpvoteView,
    top_steps,
    user_steps,
    )
from . import views
from django.contrib.auth import views as auth_view
app_name = "users"
urlpatterns = [
    path('profile/',views.profile, name ='profile' ),
    path('login/',auth_view.LoginView.as_view(template_name= 'users/login.html'), name='login'),
    path('register/',register_view, name='register'),
    path('logout/',auth_view.LogoutView.as_view(template_name= 'users/logout.html'), name='logout'),
    
    path("profile/recent-steps/",views.step_list_recent, name="step-recent"),
    path("profile/recent-steps-all/",views.step_list_recent_all, name="step-recent-all"),
    path('profile/top-steps/', views.top_steps, name='top-steps'),
    path("profile/<int:step_id>/", views.detail, name="detail"),
    path("profile/<int:step_id>/results/", views.detail, name="results"),
    path("profile/<int:step_id>/vote/", views.detail, name="vote"),
    path('profile/user-steps/<int:user_id>/', views.user_steps, name='user-steps'),

    path("profile/create-step", views.create_step, name='create_step'),
    path("profile/upvote_step/<int:pk>", UpvoteView, name ='upvote_step'),
    path("profile/todo", views.todo, name='todo'),


]
