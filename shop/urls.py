from django.urls import path

from . import views

app_name = 'shop'
urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('masters/', views.MastersView.as_view(), name='masters'),
    path('create_procedure/', views.CreateProcedure.as_view(), name='create_procedure'),
    path('', views.ProceduresView.as_view(), name='index'),
]
