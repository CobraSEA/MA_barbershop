from django.urls import path

from . import views

app_name = 'shop'
urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('reg_order/<int:proc_id>/<int:master_id>', views.reg_order, name='reg_order'),
    path('cancel_order/<int:order_id>', views.cancel_order, name='cancel_order'),
    path('set_rates/', views.set_rates, name='set_rates'),
    path('client_orders', views.ClientOrdersView.as_view(), name='client_orders'),
    path('all_orders/', views.AllOrdersView.as_view(), name='all_orders'),
    path('change_order_status/', views.change_order_status, name='change_order_status'),
    path('masters/', views.MastersView.as_view(), name='masters'),
    path('master/<int:master_id>/', views.MasterDetailView.as_view(), name='master_detail'),
    path('create_procedure/', views.CreateProcedure.as_view(), name='create_procedure'),
    path('create_comment/<int:master_id>/', views.create_new_comment, name='create_comment'),
    path('proc/<int:proc_id>/', views.ProcDetailView.as_view(), name='proc_detail'),
    path('', views.ProceduresView.as_view(), name='index'),
]
