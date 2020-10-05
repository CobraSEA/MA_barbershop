from django.contrib.auth import login, logout, authenticate, get_user_model
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from .models import Procedures, Comments


class ProceduresView(generic.ListView):
    template_name = 'shop/index.html'
    model = Procedures
    context_object_name = 'procedures_list'

    def get_queryset(self):
        query = Procedures.objects.all()
        print(query)
        return query


class CreateProcedure(generic.CreateView):
    template_name = 'shop/create_procedure.html'
    model = Procedures
    success_url = reverse_lazy('shop:index')
    fields = '__all__'


class MastersView(generic.ListView):
    template_name = 'shop/masters.html'
    context_object_name = 'masters_list'

    def get_queryset(self):
        print(get_user_model())
        return get_user_model().objects.filter(is_master=True)


class MasterDetailView(generic.DetailView):
    model = get_user_model()
    pk_url_kwarg = 'master_id'
    template_name = 'shop/master.html'
    context_object_name = 'master'


class CreateComment(generic.CreateView):
    template_name = 'shop/create_comment.html'
    model = Comments
    success_url = reverse_lazy('shop:masters')
    # fields = '__all__'
    fields = ['master', 'client', 'rate', 'text']
    hidden_fields = ['client']

    def get_initial(self):
        print(self.request.user)
        return {'client': self.request.user}

def index(request):
    return render(request, 'shop/index.html')


def user_login(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['user_name'], password=request.POST['password'])
        if user is not None:
            login(request, user)
    else:
        pass
    return HttpResponseRedirect(reverse('shop:index'))


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('shop:index'))
