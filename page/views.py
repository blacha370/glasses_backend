from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from .forms import StatusForm, LoginForm, AddOrderForm, AddMessageForm, AddMessageExtForm
from .functions import iterate_order_add, get_orders_page


def index(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='administracja').exists():
            return redirect(admin_orders, current_page=1)
        elif request.user.groups.filter(name='druk').exists():
            return redirect(user_orders, current_page=1)
        else:
            return redirect(logout_user)
    form = LoginForm(request.POST)
    return render(request, 'page/index.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['login'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                if user.groups.filter(name='administracja').exists():
                    return redirect(admin_orders, current_page=1)
                elif user.groups.filter(name='druk').exists():
                    return redirect(user_orders, current_page=1)
    messages.error(request, 'Nieprawidłowy login lub hasło')
    return redirect(index)


def logout_user(request):
    logout(request)
    messages.error(request, 'Wylogowano użytkownika')
    return redirect(index)


@login_required(login_url='')
def admin_orders(request, current_page):
    if request.user.groups.filter(name='administracja'):
        page_len = 15
        active_order_list = get_orders_page(request.user, page_len, current_page)
        if active_order_list.count() == 0 and current_page > 1:
            return redirect(admin_orders, current_page=1)
        try:
            owner = request.user.groups.exclude(name='administracja')[0]
        except IndexError:
            return redirect(logout_user)
        if not owner.name == 'Pomoc techniczna':
            orders_amount = ActiveOrder.objects.exclude(order_status='4').filter(owner=owner).count()
        else:
            orders_amount = ActiveOrder.objects.exclude(order_status='4').all().count()
        prev_page = current_page - 1
        if orders_amount > current_page * page_len:
            next_page = current_page + 1
        else:
            next_page = 0
        form = StatusForm(request.POST)
        add_order_form = AddOrderForm(request.POST)
        notification = len(Notification.objects.filter(user=request.user))
        return render(request, 'page/admin_orders.html', {'active_order_list': active_order_list, 'form': form,
                                                          'add_order_form': add_order_form, 'next_page': next_page,
                                                          'prev_page': prev_page, 'notification': notification})
    elif request.user.groups.filter(name='druk'):
        return redirect(user_orders, current_page=1)
    else:
        return redirect(logout_user)


@login_required(login_url='')
def admin_archive(request, current_page):
    if request.user.groups.filter(name='administracja'):
        page_len = 15
        notification = len(Notification.objects.filter(user=request.user))
        try:
            owner = request.user.groups.exclude(name='administracja')[0]
        except IndexError:
            return redirect(logout_user)
        if not owner.name == 'Pomoc techniczna':
            archive_order_list = ActiveOrder.objects.filter(order_status='4').filter(owner=owner)
        else:
            archive_order_list = ActiveOrder.objects.filter(order_status='4').all()
        if archive_order_list.count() == 0 and current_page > 1:
            return redirect(admin_archive, current_page=1)
        prev_page = current_page - 1
        if archive_order_list.count() > current_page * page_len:
            next_page = current_page + 1
        else:
            next_page = 0
        archive_order_list = archive_order_list[(current_page - 1) * page_len:current_page * page_len]
        return render(request, 'page/admin_archive.html', {'archive_order_list': archive_order_list,
                                                           'prev_page': prev_page, 'next_page': next_page,
                                                           'notification': notification})
    elif request.user.groups.filter(name='druk'):
        return redirect(user_archive, current_page=1)
    else:
        return redirect(logout_user)


@login_required(login_url='')
def add_order(request):
    if request.method == 'POST':
        if request.user.groups.filter(name='administracja'):
            form = AddOrderForm(request.POST, request.FILES)
            if form.is_valid():
                if str(request.FILES['file'].name).endswith('.csv'):
                    f = request.FILES['file']
                    errors = iterate_order_add(f, request)
                    if len(errors) > 0:
                        return render(request, 'page/errors.html', {'errors': errors})
                    return redirect(admin_orders, current_page=1)
        elif request.user.groups.filter(name='druk').exists():
            return redirect(user_orders, current_page=1)
    return redirect(admin_orders, current_page=1)


@login_required(login_url='')
def user_orders(request, current_page):
    if request.user.groups.filter(name='administracja') or request.user.groups.filter(name='druk'):
        page_len = 15
        orders = ActiveOrder.objects.exclude(order_status='4').exclude(order_status='5')
        if request.user.groups.filter(name='administracja') and not request.user.groups.filter(name='Pomoc techniczna'):
            try:
                owner = request.user.groups.exclude(name='administracja')[0]
                orders = orders.filter(owner=owner)
            except IndexError:
                return redirect(logout_user)
        prev_page = current_page - 1
        if orders.count() == 0 and current_page > 1:
            return redirect(user_orders, current_page=1)
        if orders.count() > current_page * page_len:
            next_page = current_page + 1
        else:
            next_page = 0
        availible_statuses = [(str(int(status[0])-1), status[1]) for status in ActiveOrder.order_statuses]
        form = StatusForm(request.POST)
        notification = len(Notification.objects.filter(user=request.user))
        active_order_list = get_orders_page(request.user, page_len, current_page)
        return render(request, 'page/user_orders.html', {'active_order_list': active_order_list, 'form': form,
                                                         'availible_statuses': availible_statuses,
                                                         'next_page': next_page, 'prev_page': prev_page,
                                                         'notification': notification})
    else:
        return redirect(logout_user)


@login_required(login_url='')
def user_archive(request, current_page):
    page_len = 15
    archive_order_list = ActiveOrder.objects.filter(order_status='4'
                                                    )[(current_page - 1) * page_len:current_page * page_len]
    orders_amount = ActiveOrder.objects.filter(order_status='4').count()
    prev_page = current_page - 1
    if orders_amount > current_page * page_len:
        next_page = current_page + 1
    else:
        next_page = 0
    notification = len(Notification.objects.filter(user=request.user))
    return render(request, 'page/user_archive.html', {'archive_order_list': archive_order_list,
                                                      'prev_page': prev_page, 'next_page': next_page,
                                                      'notification': notification})


@login_required(login_url='')
def change(request, order_id):
    order = get_object_or_404(ActiveOrder, pk=order_id)
    if request.method == 'POST' and request.user.groups.filter(name='administracja'):
        form = StatusForm(request.POST)
        if form.is_valid():
            if not order.order_status == form.cleaned_data['value']:
                status = OrderStatusChange(order=order, change_owner=request.user, previous_state=order.order_status,
                                           new_state=ActiveOrder.order_statuses[int(form.cleaned_data['value']) - 1][1])
                print(form.cleaned_data['value'])
                order.update_status(form.cleaned_data['value'])
                status.save()
        return redirect(request.META.get('HTTP_REFERER'))
    elif request.user.groups.filter(name='druk') or request.user.groups.filter(name='administracja'):
        if order.order_status == '1':
            status = OrderStatusChange(order=order, change_owner=request.user, previous_state=order.order_status,
                                       new_state=order.order_statuses[int(order.order_status)][0])
            order.order_status = order.order_statuses[int(order.order_status)][0]
            status.save()
            order.save()
            return redirect(user_orders, current_page=1)
        elif order.order_status == '3':
            return redirect(user_orders, current_page=1)
        else:
            new_state = order.order_statuses[int(order.order_status)][0]
            notification = len(Notification.objects.filter(user=request.user))
            return render(request, 'page/update_alert.html', {'order': order, 'new_state': new_state,
                                                          'notification': notification})


@login_required(login_url='')
def change_confirmation(request, order_id, order_status):
    order = get_object_or_404(ActiveOrder, pk=order_id)
    if order.order_status == order_status:
        status = OrderStatusChange(order=order, change_owner=request.user, previous_state=order.order_status,
                                   new_state=order.order_statuses[int(order.order_status)][0])
        order.update_status()
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
        admin = False
        if request.user.groups.filter(name='administracja').exists():
            admin = True
        notification = len(Notification.objects.filter(user=request.user))
    except ActiveOrder.DoesNotExist:
        if request.user.groups.filter(name='administracja').exists():
            return redirect(admin_orders, current_page=1)
        elif request.user.groups.filter(name='druk').exists():
            return redirect(user_orders, current_page=1)
    else:
        return render(request, 'page/details.html', {'order': order, 'form': form, 'status': status,
                                                     'status_changes': status_changes, 'notification': notification,
                                                     'admin': admin})


@login_required(login_url='')
def inbox(request):
    notifications = list()
    for thread in Notification.objects.filter(user=request.user).values_list('thread'):
        notifications.append(thread[0])
    message_threads = set()
    for group in request.user.groups.all():
        for thread in MessagesThread.objects.filter(archive=False).filter(groups=group).order_by('subject'):
            message_threads.add(thread)
    if request.user.groups.filter(name='administracja'):
        return render(request, 'page/admin_inbox.html', {'message_threads': message_threads,
                                                         'notifications': notifications})
    elif request.user.groups.filter(name='druk'):
        return render(request, 'page/user_inbox.html', {'message_threads': message_threads,
                                                        'notifications': notifications})


@login_required(login_url='')
def archive_inbox(request):
    message_threads = set()
    for group in request.user.groups.all():
        for thread in MessagesThread.objects.filter(archive=True).filter(groups=group).order_by('subject'):
            message_threads.add(thread)
    return render(request, 'page/archive_inbox.html', {'message_threads': message_threads})


@login_required(login_url='')
def archive_thread(request, message_topic, current_page):
    print(message_topic)
    page_len = 10
    current_notification = Notification.objects.filter(thread=message_topic)
    for notification in current_notification:
        notification.delete()
    messages_thread = MessagesThread.objects.get(pk=message_topic)
    msgs = Message.objects.filter(thread=messages_thread)
    prev_page = current_page - 1
    if msgs.count() > current_page * page_len:
        next_page = current_page + 1
    else:
        next_page = 0
    if msgs:
        msgs = msgs[(current_page - 1) * page_len:current_page * page_len]
        notification = len(Notification.objects.filter(user=request.user))
        return render(request, 'page/archive_thread.html', {'messages_thread': msgs, 'prev_page': prev_page,
                                                            'next_page': next_page, 'notification': notification})
    else:
        return redirect(archive_inbox)


@login_required(login_url='')
def message_thread(request, message_topic, current_page):
    page_len = 10
    current_notification = Notification.objects.filter(user=request.user,
                                                       thread=message_topic)
    if len(current_notification):
        current_notification.delete()
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
        notification = len(Notification.objects.filter(user=request.user))
        return render(request, 'page/message.html', {'messages_thread': messages_thread, 'form': form,
                                                     'prev_page': prev_page, 'next_page': next_page,
                                                     'notification': notification})
    else:
        return redirect(inbox)


@login_required(login_url='')
def add_message(request, thread_subject):
    if request.method == 'POST':
        form = AddMessageForm(request.POST)
        if form.is_valid():
            group_name = 'druk'
            groups = request.user.groups.exclude(name='administracja')
            groups = groups.union(Group.objects.filter(name=group_name))
            current = None
            for thread in MessagesThread.objects.filter(subject=thread_subject):
                if thread.groups.all() == groups:
                    current = thread
                    break
            if current is None:
                current = MessagesThread(subject=thread_subject)
                current.save()
                current.groups.add(*groups)
            message = Message(thread=current, message_op=request.user,
                              message_text=form.cleaned_data['message_text'])
            message.save()
            messages.info(request, 'Wysłano nową wiadomość')
            users = User.objects.filter(
                groups__name=group_name)
            for user in users:
                if request.user != user:
                    notification = Notification.objects.get_or_create(user=user, thread=current)
                    notification[0].save()
                return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='')
def new_message(request):
    form = AddMessageExtForm(request.POST)
    notification = len(Notification.objects.filter(user=request.user))
    return render(request, 'page/new_message.html', {'form': form, 'notification': notification})


@login_required(login_url='')
def add_new_message(request):
    if request.method == 'POST':
        form = AddMessageExtForm(request.POST)
        if form.is_valid():
            group_name = AddMessageExtForm.choices[int(form.cleaned_data['reciever']) - 1][1]
            groups = request.user.groups.exclude(name='administracja')
            groups = groups.union(Group.objects.filter(name=group_name))
            current = None
            for thread in MessagesThread.objects.filter(subject=form.cleaned_data['message_subject']):
                if thread.groups.all() == groups:
                    current = thread
                    break
            if current is None:
                current = MessagesThread(subject=form.cleaned_data['message_subject'])
                current.save()
                current.groups.add(*groups)
            message = Message(thread=current, message_op=request.user,
                              message_text=form.cleaned_data['message_text'])
            message.save()
            messages.info(request, 'Wysłano nową wiadomość')
            users = User.objects.filter(
                groups__name=group_name)
            for user in users:
                if request.user != user:
                    notification = Notification.objects.get_or_create(user=user, thread=current)
                    notification[0].save()
            return redirect(inbox)
    return redirect(inbox)


@login_required(login_url='')
def delete_message_thread(request, thread_id):
    if request.user.groups.filter(name='administracja'):
        try:
            thread = MessagesThread.objects.get(pk=thread_id)
            thread.delete_thread()
            messages.info(request, 'Usunięto wiadomość')
        except MessagesThread.DoesNotExist:
            messages.info(request, 'Błąd usuwania wiadomości')
            return redirect(inbox)
    return redirect(inbox)
