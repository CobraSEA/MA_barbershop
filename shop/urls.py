from django.urls import path

from . import views

app_name = 'shop'
urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('registration/<int:master_id>/', views.registration, name='registration'),
    path('client_orders', views.ClientOrdersView.as_view(), name='client_orders'),
    path('masters/', views.MastersView.as_view(), name='masters'),
    path('master/<int:master_id>/', views.MasterDetailView.as_view(), name='master_detail'),
    path('create_procedure/', views.CreateProcedure.as_view(), name='create_procedure'),
    # path('create_comment/', views.CreateComment.as_view(), name='create_comment'),
    path('create_comment/<int:master_id>/', views.create_new_comment, name='create_comment'),
    path('', views.ProceduresView.as_view(), name='index'),
]
