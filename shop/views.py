from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic

from shop.models import Procedures
from shop import forms


class ProceduresView(generic.ListView):
    template_name = 'shop/index.html'
    model = Procedures
    context_object_name = 'procedures_list'


    def get_queryset(self):
        query = Procedures.objects.all()
        print(query)
        return query


class NewUserView(generic.CreateView):
    template_name = 'shop/new_user.html'
    model = get_user_model()
    # form_class = forms.NewUserForm
    fields = ['username', 'password'
        , 'first_name', 'last_name', 'email']
    success_url = '/shop/'
    is_active = True
    is_staff = True

    def form_valid(self, form):
        return super().form_valid(form)

def new_user(request):
    if request.method == 'POST':
        pass
    else:
        render(request, 'shop/new_user.html')

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

