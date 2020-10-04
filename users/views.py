from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic


class MyUserForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("username", "password1", "password2"
                  , "email", "first_name", "last_name"
                  , "gender", "tel_number")


class CreateUserView(generic.CreateView):
    form_class = MyUserForm
    template_name = 'users/new_user.html'
    success_url = reverse_lazy('polls:index')
