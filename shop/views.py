import datetime

import pytz
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.db import transaction
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import generic
from .models import Procedures, Comments, Orders
from users.models import User
from Barber.settings import TIME_ZONE

START_WORK_HOUR = 8
END_WORK_HOUR = 23
USER_SCHEDULE_SLICE = 30


class ProceduresView(generic.ListView):
    template_name = 'shop/index.html'
    model = Procedures
    context_object_name = 'procedures_list'

    def get_queryset(self):
        query = Procedures.objects.all().order_by('-price', '-duration')
        return query


class CreateProcedure(generic.CreateView):
    template_name = 'shop/create_procedure.html'
    model = Procedures
    success_url = reverse_lazy('shop:index')
    fields = '__all__'

    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            return super().get(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('shop:index'))


class ClientOrdersView(generic.ListView):
    template_name = 'shop/your_orders.html'
    context_object_name = 'order_list'

    def get_queryset(self):
        return Orders.objects.filter(client=self.request.user.pk).order_by('start_datetime')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        rates = {}  # add rate list for user can select his choice
        for rate in Orders.RATES[:-1]:
            rt, rt_text = rate
            rates[rt] = rt_text
        context['rates'] = rates
        return context


def set_rates(request):
    if request.method == 'POST':
        if request.POST.get('rate'):
            order = Orders.objects.get(pk=request.POST['order_pk'])
            order.rate = request.POST['rate']
            order.save()
    return HttpResponseRedirect(reverse('shop:client_orders'))


class AllOrdersView(generic.ListView):
    template_name = 'shop/orders.html'
    context_object_name = 'order_list'
    model = Orders
    ordering = '-start_datetime'

    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            return super().get(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('shop:index'))


def change_order_status(request):
    """
    change status of order to selected by admin user on form All Orders
    :param request:
    :return: refresh form
    """
    if request.method == 'POST':

        # if was selected close all orders from anytime till now
        if request.POST.get('close_all'):
            now = timezone.now()
            orders = Orders.objects.select_for_update().filter(status='P', start_datetime__lte=now)
            with transaction.atomic():
                for order in orders:
                    order.status = request.POST['close_all']
                    order.save()

        # if was selected one of status for one record
        if 'change_status' in request.POST.keys():
            order = Orders.objects.get(pk=request.POST['order'])
            order.status = request.POST['change_status']
            order.save()

    return HttpResponseRedirect(reverse('shop:all_orders'))


def cancel_order(request, order_id):
    """
    cancel order by id (set status = 'C')
    :param request: not used
    :param order_id: id of selected order
    :return: refresh
    """

    order = Orders.objects.get(pk=order_id)
    if order.status == 'P':
        order.status = 'C'
        order.save()
    return HttpResponseRedirect(reverse('shop:client_orders'))


class ProcDetailView(generic.DetailView):
    template_name = 'shop/proc.html'
    context_object_name = 'procedure'
    model = Procedures
    pk_url_kwarg = 'proc_id'
    # extra_context = {'masters': User.objects.filter(is_master=True)}

    # delete me from masters list if I master
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['masters'] = User.objects.filter(is_master=True).exclude(pk=self.request.user.pk)
        return context


class MastersView(generic.ListView):
    template_name = 'shop/masters.html'
    context_object_name = 'masters_list'

    def get_queryset(self):
        return User.objects.filter(is_master=True).exclude(pk=self.request.user.pk)


class MasterDetailView(generic.DetailView):
    model = get_user_model()
    pk_url_kwarg = 'master_id'
    template_name = 'shop/master.html'
    context_object_name = 'master'
    extra_context = {'procedures': Procedures.objects.all()}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        rates = {}  # add rate list for user can select his choice
        for rate in Comments.RATES:
            rt, rt_text = rate
            rates[rt] = rt_text
        context['rates'] = rates

        masters_comments = Comments.objects.filter(master=self.object).order_by('-insert_datetime')[:10]
        comments = {}   # add 10 last comments for this master
        for c in masters_comments:
            comments[c.id] = c.client.first_name + ': ' + c.text
        context['comments'] = comments
        return context


def get_work_time_list(start):
    """
    set work time list for a day
    :return: set of datetime.datetime
    """

    if start.hour >= END_WORK_HOUR:
        start = start + datetime.timedelta(days=1)
        start = start.replace(hour=START_WORK_HOUR, minute=0, second=0, microsecond=0)

    if start.hour < START_WORK_HOUR:
        start = start.replace(hour=START_WORK_HOUR, minute=0, second=0, microsecond=0)

    if 0 < start.minute < USER_SCHEDULE_SLICE:
        start = start.replace(minute=USER_SCHEDULE_SLICE, second=0, microsecond=0)
    else:
        start = start.replace(hour=start.hour + 1, minute=0, second=0, microsecond=0)

    end = start.replace(hour=END_WORK_HOUR - 1, minute=0, second=0, microsecond=0)
    return set(
        [start + datetime.timedelta(minutes=t_minutes)
         for t_minutes in range(0, int((end - start).seconds / 60), USER_SCHEDULE_SLICE)])


def reg_order(request, proc_id, master_id):
    """
    GET: set actual time list for selected master on selected date
    POST: create order with chiced master, procedure and time
    :param request:
    :param proc_id:
    :param master_id:
    :return:
    """
    if request.method == 'GET':

        user_timezone = pytz.timezone(TIME_ZONE)
        procedure = Procedures.objects.get(pk=proc_id)
        master = User.objects.get(pk=master_id)
        context = {'procedure': procedure, 'master': master}

        if not request.GET:     # when first request.GET is empty
            now = timezone.now().astimezone(user_timezone)
            context.update({'cur_date': now.strftime("%Y-%m-%d")})
        else:       # next times when date changed get now from it
            now = datetime.datetime.strptime(request.GET['cur_date'], "%Y-%m-%d").astimezone(user_timezone)
            now += datetime.timedelta(days=int(request.GET['change_date']))
            now = now.replace(hour=START_WORK_HOUR, minute=0, second=0, microsecond=0)
            if now < timezone.now().astimezone(user_timezone):
                now = timezone.now().astimezone(user_timezone)
            context.update({'cur_date': now.strftime("%Y-%m-%d")})

        # take all orders when master will busy
        master_ordered_times = Orders.objects.filter(master=master_id, start_datetime__gte=now, status='P')

        # set time steps when master is busy
        time_list = get_work_time_list(now)
        time_stop_list = set(
            [time for time in time_list for m_time in master_ordered_times if m_time.start_datetime <= time <= m_time.end_datetime]
        )

        # delete them from available time list
        time_list = list(time_list - time_stop_list)
        time_list.sort()

        times = {}
        for time in time_list:
            times[time.strftime('%H:%M')] = time.strftime("%Y-%m-%d %H:%M")

        context.update({'times': times})
        return render(request, 'shop/reg_order.html', context)
    else:
        date = datetime.datetime.strptime(request.POST['reg_date'], "%Y-%m-%d %H:%M")
        if request.user.is_authenticated:
            d = Orders(master_id=request.POST['master_id']
                       , client=request.user
                       , procedure_id=request.POST['proc_id']
                       , start_datetime=date
                       )
            d.save()
        return redirect('shop:client_orders')


# class CommentForm(ModelForm):
#     master = ModelChoiceField(queryset=User.objects.filter(is_master=True), required=True)
#
#     class Meta:
#         model = Comments
#         fields = ['master', 'rate', 'text']
#         hidden_fields = ['client']


def create_new_comment(request, master_id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            comment = Comments(master_id=master_id, rate=request.POST['rate']
                               , client=request.user, text=request.POST['comment_text'])
            comment.save()
        return HttpResponseRedirect(reverse('shop:master_detail', args=[master_id]))
    # else:
        # form = CommentForm()
        # context = {'form': form}
        # template_name = 'shop/create_comment.html'

        # return render(request, template_name, context)


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
