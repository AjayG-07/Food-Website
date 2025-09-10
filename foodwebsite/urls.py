"""
URL configuration for foodwebsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from app1 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("captcha/", include("captcha.urls")),
    path('', views.home_view,name='home' ),
    path("food/",views.food_view,name='food'),
    path("list/",views.food_list,name='list'),
    path("user/",views.user_food_list,name='user'),
    path("details/<int:id>/",views.food_details,name='details'),
    path('update/<int:id>/', views.food_update, name='update'),
    path('delete/<int:id>/', views.food_delete, name='delete'),

    # Food Cart 

    path('food_cart_view/', views.food_cart_view, name='food_cart_view'),
    path('add_to_cart/<int:id>/', views.food_add_cart, name='add_to_cart'),
    path('remove_cart/<int:id>/', views.food_remove_view , name='remove_from_cart'),
    path('clear_cart/', views.food_clear_view , name='clear_cart'),

    path('cart/increase/<int:food_id>/', views.increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:food_id>/', views.decrease_quantity, name='decrease_quantity'),


    # login setup

    path('signup/', views.signup_view , name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'), 
    path('foodadmin/', views.admin_sign_view, name='food_sign'),
    path('dashboard/', views.food_dashboard_view, name='food_dashboard'),
    
  

 
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
