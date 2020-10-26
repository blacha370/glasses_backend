from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from .forms import StatusForm, LoginForm, AddOrderForm, AddMessageForm, AddMessageExtForm
from .functions import iterate_order_add, get_orders_page


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
        active_order_list = get_orders_page(request.user, ActiveOrder, page_len, current_page)
        owner = request.user.groups.exclude(name='administracja')[0]
        if not owner.name == 'Pomoc techniczna':
            orders_amount = ActiveOrder.objects.filter(owner=owner).count()
        else:
            orders_amount = ActiveOrder.objects.all().count()
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
        archive_order_list = get_orders_page(request.user, UnactiveOrder, page_len, current_page)
        orders_amount = UnactiveOrder.objects.count()
        prev_page = current_page - 1
        if orders_amount > current_page * page_len:
            next_page = current_page + 1
        else:
            next_page = 0
        notification = len(Notification.objects.filter(user=request.user))
        return render(request, 'page/admin_archive.html', {'archive_order_list': archive_order_list,
                                                           'prev_page': prev_page, 'next_page': next_page,
                                                           'notification': notification})
    elif request.user.groups.filter(name='druk'):
        return redirect(user_archive, current_page=1)


@login_required(login_url='')
def add_order(request):
    if request.user.groups.filter(name='administracja'):
        if request.method == 'POST':
            form = AddOrderForm(request.POST, request.FILES)
            if form.is_valid():
                if str(request.FILES['file'].name).endswith('.csv'):
                    f = request.FILES['file']
                    errors = iterate_order_add(f, request)
                    if len(errors) > 0:
                        return render(request, 'page/errors.html', {'errors': errors})
                    return redirect(admin_orders, current_page=1)
        form = AddOrderForm(request.POST)
        return render(request, 'page/add_order.html', {'form': form})
    elif request.user.groups.filter(name='druk').exists():
        return redirect(user_orders, current_page=1)


@login_required(login_url='')
def user_orders(request, current_page):
    page_len = 15
    orders_amount = ActiveOrder.objects.count()
    prev_page = current_page - 1
    if orders_amount > current_page * page_len:
        next_page = current_page + 1
    else:
        next_page = 0
    availible_statuses = list()
    first = True
    for status in ActiveOrder.order_statuses:
        if first:
            first = False
            continue
        else:
            availible_statuses.append((str(int(status[0])-1), status[1]))
    form = StatusForm(request.POST)
    notification = len(Notification.objects.filter(user=request.user))
    active_order_list = get_orders_page(request.user, ActiveOrder, page_len, current_page)
    return render(request, 'page/user_orders.html', {'active_order_list': active_order_list, 'form': form,
                                                     'availible_statuses': availible_statuses, 'next_page': next_page,
                                                     'prev_page': prev_page, 'notification': notification})


@login_required(login_url='')
def user_archive(request, current_page):
    page_len = 15
    archive_order_list = get_orders_page(request.user, UnactiveOrder, page_len, current_page)
    orders_amount = UnactiveOrder.objects.count()
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
        if order.order_status == '1':
            status = OrderStatusChange(order=order, change_owner=request.user.username,
                                       previous_state=order.order_status,
                                       new_state=order.order_statuses[int(order.order_status)][0],
                                       date=dateformat.format(timezone.now(), 'H:i d.m.y'))
            order.order_status = order.order_statuses[int(order.order_status)][0]
            status.save()
            order.save()
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
        for thread in MessagesThread.objects.filter(reciever=group).order_by('subject'):
            message_threads.add(thread)
        for thread in MessagesThread.objects.filter(creator=group).order_by('subject'):
            message_threads.add(thread)
    if request.user.groups.filter(name='administracja'):
        return render(request, 'page/admin_inbox.html', {'message_threads': message_threads,
                                                         'notifications': notifications})
    elif request.user.groups.filter(name='druk'):
        return render(request, 'page/user_inbox.html', {'message_threads': message_threads,
                                                        'notifications': notifications})


@login_required(login_url='')
def archive_inbox(request):
    message_threads = ArchiveThread.objects.order_by('subject')
    return render(request, 'page/archive_inbox.html', {'message_threads': message_threads})


@login_required(login_url='')
def archive_thread(request, message_topic, current_page):
    page_len = 10
    current_notification = Notification.objects.filter(user=request.user,
                                                       thread=message_topic)
    if len(current_notification):
        current_notification.delete()
    messages_thread = ArchiveMessage.objects.filter(thread=message_topic)
    messages_thread = messages_thread.order_by('pk').reverse()
    prev_page = current_page - 1
    if len(messages_thread) > current_page * page_len:
        next_page = current_page + 1
    else:
        next_page = 0
    if messages_thread:
        messages_thread = messages_thread[(current_page - 1) * page_len:current_page * page_len]
        notification = len(Notification.objects.filter(user=request.user))
        return render(request, 'page/archive_thread.html', {'messages_thread': messages_thread, 'prev_page': prev_page,
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
            try:
                thread = MessagesThread.objects.get_or_create(subject=thread_subject, defaults={
                    'creator': Group.objects.get(name='druk'),
                    'reciever': ActiveOrder.objects.get(order_number=thread_subject).owner})
            except ActiveOrder.DoesNotExist:
                thread = MessagesThread.objects.get_or_create(subject=thread_subject)
            thread[0].save()
            message = Message(thread=thread[0], message_text=form.cleaned_data['message_text'],
                              message_op=request.user.username,
                              message_date=dateformat.format(timezone.now(), 'H:i d.m.y'))
            message.save()
            messages.info(request, 'Wysłano nową wiadomość')
            group = list()
            try:
                group = ActiveOrder.objects.get(order_number=thread_subject).owner
            except ActiveOrder.DoesNotExist:
                group = group.objects.get(name='administracja')
            finally:
                users = User.objects.filter(groups__name=group)
                workers = User.objects.filter(groups__name='druk')
                users = users.union(workers)
                for user in users:
                    if user == request.user:
                        continue
                    notification = Notification.objects.get_or_create(user=user, thread=thread[0])
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
            group_name = AddMessageExtForm.choices[int(form.cleaned_data['reciever'])-1][1]
            try:
                thread = MessagesThread.objects.get_or_create(subject=form.cleaned_data['message_subject'], defaults={
                    'creator': request.user.groups.exclude(name='administracja')[0],
                    'reciever': Group.objects.get(name=group_name)})
            except IndexError:
                thread = MessagesThread.objects.get_or_create(subject=form.cleaned_data['message_subject'], defaults={
                    'creator': request.user.groups.get(name='administracja'),
                    'reciever': Group.objects.get(name=group_name)})
            finally:
                thread = thread[0]
                if not request.user.groups.filter(name=thread.creator) and \
                        not request.user.groups.filter(name=thread.reciever):
                    try:
                        thread = MessagesThread(subject=form.cleaned_data['message_subject'] + '.1',
                                                creator=request.user.groups.exclude(name='administracja')[0],
                                                reciever=Group.objects.get(name=group_name))
                    except IndexError:
                        thread = MessagesThread(subject=form.cleaned_data + '.1',
                                                creator=request.user.groups.get(name='administracja'),
                                                reciever=Group.objects.get(name=group_name))
                thread.save()
                message = Message(thread=thread, message_text=form.cleaned_data['message_text'],
                                  message_op=request.user.username,
                                  message_date=dateformat.format(timezone.now(), 'H:i d.m.y'))
                message.save()
                messages.info(request, 'Wysłano nową wiadomość')
                users = get_user_model()
                users = users.objects.filter(
                    groups__name=group_name)
                for user in users:
                    if request.user != user:
                        notification = Notification.objects.get_or_create(user=user, thread=thread)
                        notification[0].save()
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
