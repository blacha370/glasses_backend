from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone, dateformat
from .models import ActiveOrder, UnactiveOrder, Message, MessagesThread, OrderStatusChange
from .forms import StatusForm, LoginForm, AddOrderForm, AddMessageForm, AddMessageExtForm
from .functions import iterate_order_add


def index(request):
    if request.user.is_authenticated:
        return redirect(admin_orders, current_page=1)
    form = LoginForm(request.POST)
    return render(request, 'page/index.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['login'], password=form.cleaned_data['password'])
            if user:
                login(request, user)
                if user.groups.filter(name='administracja').exists():
                    return redirect(admin_orders, current_page=1)
                elif user.groups.filter(name='druk').exists():
                    return redirect(user_orders, current_page=1)
    form = LoginForm(request.POST)
    return render(request, 'page/index.html', {'form': form, 'message': "Błędny login lub hasło"})


def logout_user(request):
    logout(request)
    form = LoginForm(request.POST)
    return render(request, 'page/index.html', {'form': form, 'message': "Pomyślnie wylogowano"})


@login_required(login_url='')
def admin_orders(request, current_page):
    if request.user.groups.filter(name='administracja'):
        page_len = 30
        active_order_list = ActiveOrder.objects.order_by('order_status')
        prev_page = current_page - 1
        if len(active_order_list) > current_page * page_len:
            next_page = current_page + 1
        else:
            next_page = 0
        active_order_list = active_order_list.reverse()
        active_order_list = active_order_list[(current_page-1) * page_len: current_page * page_len]
        form = StatusForm(request.POST)
        add_order_form = AddOrderForm(request.POST)
        return render(request, 'page/admin_orders.html', {'active_order_list': active_order_list, 'form': form,
                                                          'add_order_form': add_order_form, 'next_page': next_page,
                                                          'prev_page': prev_page})
    elif request.user.groups.filter(name='druk'):
        return redirect(user_orders, current_page=1)


@login_required(login_url='')
def admin_archive(request, current_page):
    if request.user.groups.filter(name='administracja'):
        page_len = 30
        archive_order_list = UnactiveOrder.objects.order_by('-pub_date')
        prev_page = current_page - 1
        if len(archive_order_list) > current_page * page_len:
            next_page = current_page + 1
        else:
            next_page = 0
        archive_order_list = archive_order_list[(current_page - 1) * page_len : current_page * page_len]
        return render(request, 'page/admin_archive.html', {'archive_order_list': archive_order_list,
                                                           'prev_page': prev_page, 'next_page': next_page})
    elif request.user.groups.filter(name='druk'):
        return redirect(user_orders, current_page=1)


@login_required(login_url='')
def add_order(request):
    if request.user.groups.filter(name='administracja'):
        if request.method == 'POST':
            form = AddOrderForm(request.POST, request.FILES)
            if form.is_valid():
                if str(request.FILES['file'].name).endswith('.csv'):
                    f = request.FILES['file']
                    iterate_order_add(f, request)
                    return redirect(admin_orders, current_page=1)
        form = AddOrderForm(request.POST)
        return render(request, 'page/add_order.html', {'form': form})
    elif request.user.groups.filter(name='druk').exists():
        return redirect(user_orders, current_page=1)


@login_required(login_url='')
def user_orders(request, current_page):
    page_len = 30
    active_order_list = ActiveOrder.objects.order_by('order_status')
    active_order_list = active_order_list.exclude(order_status='5')
    active_order_list = active_order_list.reverse()
    prev_page = current_page - 1
    if len(active_order_list) > current_page * page_len:
        next_page = current_page + 1
    else:
        next_page = 0
    active_order_list = active_order_list[(current_page - 1) * page_len: current_page * page_len]
    availible_statuses = list()
    first = True
    for status in ActiveOrder.order_statuses:
        if first:
            first = False
            continue
        else:
            availible_statuses.append((str(int(status[0])-1), status[1]))
    form = StatusForm(request.POST)
    return render(request, 'page/user_orders.html', {'active_order_list': active_order_list, 'form': form,
                                                     'availible_statuses': availible_statuses, 'next_page': next_page,
                                                          'prev_page': prev_page})


@login_required(login_url='')
def user_archive(request, current_page):
    page_len = 30
    archive_order_list = UnactiveOrder.objects.order_by('-pub_date')
    prev_page = current_page - 1
    if len(archive_order_list) > current_page * page_len:
        next_page = current_page + 1
    else:
        next_page = 0
    archive_order_list = archive_order_list[(current_page - 1) * page_len: current_page * page_len]
    return render(request, 'page/user_archive.html', {'archive_order_list': archive_order_list,
                                                      'prev_page': prev_page, 'next_page': next_page})


@login_required(login_url='')
def change(request, order_id):
    order = get_object_or_404(ActiveOrder, pk=order_id)
    if request.method == 'POST':
        form = StatusForm(request.POST)
        if form.is_valid():
            if not order.order_status == form.cleaned_data['value']:
                status = OrderStatusChange(order=order, change_owner=request.user.username,
                                           previous_state=order.order_status, new_state=form.cleaned_data['value'],
                                           date=dateformat.format(timezone.now(), 'H:i d.m.y'))
                order.order_status = form.cleaned_data['value']
                status.save()
                order.save()
        return redirect(request.META.get('HTTP_REFERER'))
    elif request.user.groups.filter(name='druk') or request.user.groups.filter(name='administracja'):
        new_state = order.order_statuses[int(order.order_status)][0]
        return render(request, 'page/update_alert.html', {'order': order, 'new_state': new_state})


@login_required(login_url='')
def change_confirmation(request, order_id, order_status):
    order = get_object_or_404(ActiveOrder, pk=order_id)
    if order.order_status == order_status:
        status = OrderStatusChange(order=order, change_owner=request.user.username,
                                   previous_state=order.order_status,
                                   new_state=order.order_statuses[int(order.order_status)][0],
                                   date=dateformat.format(timezone.now(), 'H:i d.m.y'))
        order.order_status = order.order_statuses[int(order.order_status)][0]
        status.save()
        order.save()
    return redirect(user_orders, current_page=1)


@login_required(login_url='')
def details(request, order_id):
    try:
        order = ActiveOrder.objects.get(pk=order_id)
        status_changes = OrderStatusChange.objects.filter(order=order)
        status = ActiveOrder.order_statuses[int(order.order_status) - 1][1]
        form = AddMessageForm(request.POST)
    except ActiveOrder.DoesNotExist:
        if request.user.groups.filter(name='administracja').exists():
            return redirect(admin_orders, current_page=1)
        elif request.user.groups.filter(name='druk').exists():
            return redirect(user_orders, current_page=1)
    else:
        return render(request, 'page/details.html', {'order': order, 'form': form, 'status': status,
                                                     'status_changes': status_changes})


@login_required(login_url='')
def inbox(request):
    message_threads = MessagesThread.objects.order_by('subject')
    if request.user.groups.filter(name='administracja'):
        return render(request, 'page/admin_inbox.html', {'message_threads': message_threads})
    elif request.user.groups.filter(name='druk'):
        return render(request, 'page/user_inbox.html', {'message_threads': message_threads})
    else:
        return redirect(user_orders, current_page=1)


@login_required(login_url='')
def message_thread(request, message_topic, current_page):
    page_len = 10
    messages_thread = Message.objects.filter(thread=message_topic)
    messages_thread = messages_thread.order_by('pk').reverse()
    prev_page = current_page - 1
    if len(messages_thread) > current_page * page_len:
        next_page = current_page + 1
    else:
        next_page = 0
    if messages_thread:
        messages_thread = messages_thread[(current_page - 1) * page_len:current_page * page_len]
        form = AddMessageForm(request.POST)
        return render(request, 'page/message.html', {'messages_thread': messages_thread, 'form': form,
                                                     'prev_page': prev_page, 'next_page': next_page})
    else:
        return redirect(inbox)


@login_required(login_url='')
def add_message(request, thread_subject):
    if request.method == 'POST':
        form = AddMessageForm(request.POST)
        if form.is_valid():
            thread = MessagesThread.objects.get_or_create(subject=thread_subject)
            thread[0].save()
            message = Message(thread=thread[0], message_text=form.cleaned_data['message_text'],
                              message_op=request.user.username,
                              message_date=dateformat.format(timezone.now(), 'H:i d.m.y'))
            message.save()
            return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='')
def new_message(request):
    form = AddMessageExtForm(request.POST)
    return render(request, 'page/new_message.html', {'form': form})


@login_required(login_url='')
def add_new_message(request):
    if request.method == 'POST':
        form = AddMessageExtForm(request.POST)
        if form.is_valid():
            thread = MessagesThread.objects.get_or_create(subject=form.cleaned_data['message_subject'])
            thread[0].save()
            message = Message(thread=thread[0], message_text=form.cleaned_data['message_text'],
                              message_op=request.user.username,
                              message_date=dateformat.format(timezone.now(), 'H:i d.m.y'))
            message.save()
            return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='')
def delete_message_thread(request, thread_id):
    if request.user.groups.filter(name='administracja'):
        thread = MessagesThread.objects.get(pk=thread_id)
        thread.delete()
    return redirect(inbox)
