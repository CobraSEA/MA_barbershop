from django.contrib.auth.forms import UserCreationForm
from users.models import User

class MyUserForm(UserCreationForm):
    class Meta:
        model = User
        # model = get_user_model()
        fields = ("username", "password1", "password2"
                  , "email", "first_name", "last_name"
                  , "gender", "tel_number", 'birthday')


