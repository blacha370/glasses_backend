from .models import ActiveOrder, UnactiveOrder, OrderStatusChange
from django.utils import timezone, dateformat
from django.contrib.auth.models import Group


def iterate_order_add(f, request):
    info = list()
    all_orders = set()
    for order in ActiveOrder.objects.all():
        all_orders.add(order.order_number)
    for order in UnactiveOrder.objects.all():
        all_orders.add(order.order_number)
    first = True
    i = 1
    for row in f:
        if first:
            first = False
            continue
        line = str(row)
        line = line[2:-5]
        if line.replace(';', '') == '' or line.replace(',', '') == '':
            info.append('pusta linia: ' + str(i))
        elif ';' in line:
            line = line.split(';')
            if not line[1] in all_orders:
                create_order(line, request)
        elif ',' in line:
            line = line.split(',')
            if not line[1] in all_orders:
                create_order(line, request)
        else:
            info.append('błąd z linią: ' + str(i))
        i += 1
    return info


def get_orders_page(user, orders_type: object, page_len: int, current_page: int):
    try:
        user_group = user.groups.exclude(name='administracja')[0]
    except IndexError:
        order_list = orders_type.objects.all().count()
        if order_list <= page_len:
            return orders_type.objects.order_by('order_status', '-pub_date').reverse()
        elif order_list > (current_page - 1) * page_len:
            orders = orders_type.objects.order_by('order_status', '-pub_date').reverse()
            return orders[(current_page - 1) * page_len:current_page * page_len]
    else:
        if user_group.name == 'druk':
            order_list = orders_type.objects.all().count()
            if order_list <= page_len:
                orders = orders_type.objects.order_by('order_status', '-pub_date').reverse()
                return orders[(current_page - 1) * page_len:current_page * page_len]
            elif order_list > (current_page - 1) * page_len:
                orders = orders_type.objects.order_by('order_status', '-pub_date').reverse()
                return orders[(current_page - 1) * page_len:current_page * page_len]
        elif user_group.name == 'Pomoc techniczna':
            order_list = orders_type.objects.all().count()
            if order_list <= page_len:
                orders = orders_type.objects.order_by('order_status', '-pub_date').reverse()
                return orders[(current_page - 1) * page_len:current_page * page_len]
            elif order_list > (current_page - 1) * page_len:
                orders = orders_type.objects.order_by('order_status', '-pub_date').reverse()
                return orders[(current_page - 1) * page_len:current_page * page_len]
        else:
            order_list = orders_type.objects.filter(owner=user_group).count()
            if order_list <= page_len:
                orders = orders_type.objects.filter(owner=user_group)
                orders = orders.order_by('order_status', '-pub_date').reverse()
                return orders[(current_page - 1) * page_len:current_page * page_len]
            elif order_list > (current_page - 1) * page_len:
                orders = orders_type.objects.filter(owner=user_group)
                orders = orders.order_by('order_status', '-pub_date').reverse()
                return orders[(current_page - 1) * page_len:current_page * page_len]


def get_order_owner(order_number):
    if order_number.startswith('A20'):
        return Group.objects.get(name='besart')
    elif order_number.startswith('AU'):
        return Group.objects.get(name='kasia')
    elif order_number.startswith('4DICH'):
        return Group.objects.get(name='4dich')
    elif order_number.startswith('Coś'):
        return Group.objects.get(name='szymon')
    else:
        return None


def create_order(line, request):
    owner = get_order_owner(line[1])
    if len(line) == 5:
        if line[3].startswith('1'):
            order = ActiveOrder(order_number=line[1], order_status='1', pub_date=line[0],
                                image=line[2].replace('.jpg', ''), divided='całe',
                                owner=owner, tracking_number=line[4])
        elif line[3].startswith('2'):
            order = ActiveOrder(order_number=line[1], order_status='1', pub_date=line[0],
                                image=line[2].replace('.jpg', ''), divided='połówka',
                                owner=owner)
        else:
            order = ActiveOrder(order_number=line[1], order_status='1', pub_date=line[0],
                                image=line[2].replace('.jpg', ''),
                                owner=owner)
    elif len(line) == 4:
        if line[3].startswith('1'):
            order = ActiveOrder(order_number=line[1], order_status='1', pub_date=line[0],
                                image=line[2].replace('.jpg', ''), divided='całe',
                                owner=owner)
        elif line[3].startswith('2'):
            order = ActiveOrder(order_number=line[1], order_status='1', pub_date=line[0],
                                image=line[2].replace('.jpg', ''), divided='połówka',
                                owner=owner)
        else:
            order = ActiveOrder(order_number=line[1], order_status='1', pub_date=line[0],
                                image=line[2].replace('.jpg', ''),
                                owner=owner)
    elif len(line) == 3:
        if line[3].endswith('.jpg'):
            order = ActiveOrder(order_number=line[1], order_status='1', pub_date=line[0],
                                image=line[2].replace('.jpg', ''), divided='brak',
                                owner=owner)
        else:
            if line[2].startswith('1'):
                order = ActiveOrder(order_number=line[1], order_status='1', pub_date=line[0],
                                    divided='całe', owner=owner)
            elif line[2].startswith('2'):
                order = ActiveOrder(order_number=line[1], order_status='1', pub_date=line[0],
                                    divided='połówka', owner=owner)
            else:
                order = ActiveOrder(order_number=line[1], order_status='1', pub_date=line[0],
                                    owner=owner)
    else:
        order = ActiveOrder(order_number=line[1], order_status='1', pub_date=line[0],
                            owner=owner)
    status = OrderStatusChange(order=order, change_owner=request.user.username,
                               previous_state='1', new_state='1',
                               date=dateformat.format(timezone.now(), 'H:i d.m.y'))
    order.save()
    status.save()
