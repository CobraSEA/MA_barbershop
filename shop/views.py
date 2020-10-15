import datetime

import pytz
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.forms import ModelForm, ModelChoiceField
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import generic
from .models import Procedures, Comments, Orders
from users.models import User
from Barber.settings import TIME_ZONE


class ProceduresView(generic.ListView):
    template_name = 'shop/index.html'
    model = Procedures
    context_object_name = 'procedures_list'

    def get_queryset(self):
        query = Procedures.objects.all()
        return query


class CreateProcedure(generic.CreateView):
    template_name = 'shop/create_procedure.html'
    model = Procedures
    success_url = reverse_lazy('shop:index')
    fields = '__all__'

    def get(self, request, *args, **kwargs):
        print(request.user.is_staff)
        if request.user.is_staff:
            return super().get(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('shop:index'))


class ClientOrdersView(generic.ListView):
    template_name = 'shop/your_orders.html'
    context_object_name = 'order_list'

    def get_queryset(self):
        return Orders.objects.filter(client=self.request.user.pk)


class AllOrdersView(generic.ListView):
    template_name = 'shop/orders.html'
    context_object_name = 'order_list'
    model = Orders
    ordering = 'start_datetime'

    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            return super().get(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('shop:index'))


def change_order_status(request):
    print('change_order_status', request.POST)
    order = Orders.objects.get(pk=request.POST['order'])
    order.status = request.POST['change_status']
    order.save()
    return HttpResponseRedirect(reverse('shop:all_orders'))


class ProcDetailView(generic.DetailView):
    template_name = 'shop/proc.html'
    context_object_name = 'procedure'
    model = Procedures
    pk_url_kwarg = 'proc_id'
    extra_context = {'masters': User.objects.filter(is_master=True)}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        return context


class MastersView(generic.ListView):
    template_name = 'shop/masters.html'
    context_object_name = 'masters_list'

    def get_queryset(self):
        return User.objects.filter(is_master=True)


class MasterDetailView(generic.DetailView):
    model = get_user_model()
    pk_url_kwarg = 'master_id'
    template_name = 'shop/master.html'
    context_object_name = 'master'
    extra_context = {'procedures': Procedures.objects.all()}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        masters_comments = Comments.objects.filter(master=self.object).order_by('-insert_datetime')[:10]
        context['master_age'] = datetime.datetime.now().date().year - self.object.birthday.year

        comments = {}
        for c in masters_comments:
            comments[c.id] = c.client.first_name + ': ' + c.text
        context['comments'] = comments
        return context


# def registration(request):
#     if request.method == 'POST':



class RegOrderForm(ModelForm):
    class Meta:
        model = Orders
        fields = ['start_datetime']

def reg_order(request, proc_id, master_id):
    if request.method == 'GET':
        form = RegOrderForm()
        form.start = timezone.now()

        user_timezone = pytz.timezone(TIME_ZONE)

        context = {'form': form}
        procedure = Procedures.objects.get(pk=proc_id)
        master = User.objects.get(pk=master_id)
        context.update({'procedure': procedure, 'master': master})

        now = timezone.now().astimezone(user_timezone)
        if now.hour >= 23:
            now = datetime.datetime(now.year, now.month, now.day, 8, 0).astimezone(user_timezone)

        master_exec_times = Orders.objects.filter(master=master_id, start_datetime__gte=now)
        time_ex_list = [ex_time.start_datetime.astimezone(user_timezone) for ex_time in master_exec_times]

        times = {}
        time = datetime.datetime(now.year, now.month, now.day, now.hour + 1, 0).astimezone(user_timezone)
        for i in range(now.hour + 1, 23, 1):
            if time not in time_ex_list:
                times[time.strftime('%H:%M')] = time.strftime("%Y-%m-%d %H:%M")
            time += datetime.timedelta(hours=1)
            # print(time.strftime('%H:%M'))
        context.update({'times': times})

        return render(request, 'shop/reg_order.html', context)
    else:
        # print(request.POST)
        date = datetime.datetime.strptime(request.POST['reg_date'], "%Y-%m-%d %H:%M")
        print(date)
        d = Orders(master_id=request.POST['master_id'],
                              client=request.user,
                              procedure_id=request.POST['proc_id'],
                              start_datetime=date)
        print(d.start_datetime)
        d.save()
        return redirect('shop:client_orders')



class CommentForm(ModelForm):
    master = ModelChoiceField(queryset=User.objects.filter(is_master=True), required=True)

    class Meta:
        model = Comments
        fields = ['master', 'rate', 'text']
        hidden_fields = ['client']


def create_new_comment(request, master_id):
    if request.method == 'POST':
        print(dir(request))
        print(master_id, request.POST)
        comment = Comments(master_id=master_id
                           , client=request.user, text=request.POST['comment_text'])
        comment.save()
        return HttpResponseRedirect(reverse('shop:master_detail', args=[master_id]))
    else:
        form = CommentForm()
        context = {'form': form}
        template_name = 'shop/create_comment.html'

    return render(request, template_name, context)


class CreateComment(generic.CreateView):
    template_name = 'shop/create_comment.html'
    model = Comments
    success_url = reverse_lazy('shop:masters')
    # fields = '__all__'
    fields = ['master', 'rate', 'text']
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
