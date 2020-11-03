from django.contrib.auth import get_user_model, login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy, reverse
from django.views import generic
from users.forms import MyUserForm
from users.models import User
from shop.models import MasterProcedure, Procedures



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
    fields = ['is_master', 'is_staff', 'nick_name', 'level']
    success_url = reverse_lazy('users:all_users')
    template_name = 'users/user_update.html'
    extra_context = {'procedures': Procedures.objects.all()}

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        master_proc = [t.procedure_id for t in MasterProcedure.objects.filter(master=self.object)]
        master_procedure = {}
        for p in context['procedures']:
            master_procedure[p.name] = p.pk in master_proc
        context['master_proc'] = master_procedure
        context.pop('user')
        return context

    def post(self, request, *args, **kwargs):
        result = super().post(request, *args, **kwargs)
        if self.object.is_master:
            kw = self.get_form_kwargs()
            proc_all = [pr.name for pr in self.extra_context['procedures']]
            proc_list = [name for name in kw['data'].keys() if name in proc_all]

            MasterProcedure.objects.filter(master=self.object).delete()
            for p in self.extra_context['procedures']:
                if p.name in proc_list:
                    MasterProcedure.objects.create(master=self.object, procedure=p)

        return result
