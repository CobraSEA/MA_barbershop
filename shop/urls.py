from django.urls import path

from . import views

app_name = 'shop'
urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('new_user/', views.NewUserView.as_view(), name='new_user'),
    path('', views.ProceduresView.as_view(), name='index'),
]
