from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('registration/', views.CreateUserView.as_view(), name='registration'),
    path('all_users/', views.AllUsersView.as_view(), name='all_users'),
    path('update_user/<int:pk>', views.UserUpdateView.as_view(), name='user_update'),
]