from django.urls import path

from . import views

app_name = 'shop'
urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('', views.ProceduresView.as_view(), name='index'),
]
