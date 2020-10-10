from django.contrib.auth import get_user_model, login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
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
    ordering = ['username', 'is_staff', 'is_master', 'first_name', 'last_name']

    def get_queryset(self):
        return User.objects.all()

class UserUpdateView(generic.edit.UpdateView):
    model = User
    fields = ['is_master', 'is_staff', 'nick_name']
    template_name_suffix = '_update'
    pk_url_kwarg = 'user_id'
    context_object_name = 'users'
