from django.contrib.auth import get_user_model, login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy, reverse
from django.views import generic
from users.forms import MyUserForm
from users.models import User

class CreateUserView(generic.CreateView):
    form_class = MyUserForm
    template_name = 'users/new_user.html'
    success_url = reverse_lazy('shop:index')

    def post(self, request, *args, **kwargs):
        create_user = super().post(request, *args, **kwargs)
        if self.object:
            login(request, self.object)
        return create_user


class AllUsersView(generic.ListView):
    template_name = 'users/all_users.html'
    model = get_user_model()
    fields = '__all__'
    context_object_name = 'users'
    ordering = ['is_staff', 'is_master', 'username', 'first_name', 'last_name']

    def get_queryset(self):
        return User.objects.all().order_by('-is_staff', '-is_master', 'username', 'first_name', 'last_name')


class UserUpdateView(generic.edit.UpdateView):
    model = User
    fields = ['is_master', 'is_staff', 'nick_name']
    success_url = reverse_lazy('users:all_users')
    template_name = 'users/user_update.html'



