from django.contrib.auth import get_user_model, login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic


class MyUserForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        # fields = '__all__'
        fields = ("username", "password1", "password2"
                  , "email", "first_name", "last_name"
                  , "gender", "tel_number", 'is_master'
                  , 'birthday', 'level', 'nick_name')


class CreateUserView(generic.CreateView):
    form_class = MyUserForm
    template_name = 'users/new_user.html'
    success_url = reverse_lazy('shop:index')

    def post(self, request, *args, **kwargs):
        create_user = super().post(request, *args, **kwargs)
        if self.object:
            login(request, self.object)
        return create_user