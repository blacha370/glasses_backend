from .models import ActiveOrder, OrderStatusChange
from datetime import date
from django.contrib.auth.models import Group


def iterate_order_add(f, request):
    info = list()
    all_orders = set()
    for order in ActiveOrder.objects.all():
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
            line = line.split(',')
            if not line[1] in all_orders:
                owner = get_order_owner(line[1])
                if owner:
                    create_order(line, request, owner)
                else:
                    info.append('[{0}] '.format(i) + 'nieprawidłowy numer zamówienia: ' + line[1])
        elif ',' in line:
            line = line.split(',')
            if not line[1] in all_orders:
                owner = get_order_owner(line[1])
                if owner:
                    create_order(line, request, owner)
                else:
                    info.append('[{0}] '.format(i) + 'nieprawidłowy numer zamówienia: ' + line[1])
        else:
            info.append('błąd z linią: ' + str(i))
        i += 1
    return info


def get_orders_page(user, page_len: int, current_page: int):
    orders = ActiveOrder.objects.exclude(order_status='4').order_by('order_status', 'pub_date').reverse()
    if Group.objects.get(name='druk') in user.groups.all():
        return orders.exclude(order_status='5')[(current_page-1) * page_len:current_page * page_len]
    elif Group.objects.get(name='4dich') in user.groups.all():
        return orders.filter(owner=Group.objects.get(name='4dich'))[(current_page-1) * page_len:current_page * page_len]
    elif Group.objects.get(name='besart') in user.groups.all():
        return orders.filter(owner=Group.objects.get(name='besart')
                             )[(current_page-1) * page_len:current_page * page_len]
    elif Group.objects.get(name='kasia') in user.groups.all():
        return orders.filter(owner=Group.objects.get(name='kasia'))[(current_page-1) * page_len:current_page * page_len]
    elif Group.objects.get(name='Pomoc techniczna') in user.groups.all():
        return orders[(current_page-1) * page_len:current_page * page_len]
    else:
        return ActiveOrder.objects.none()


def get_order_owner(order_number):
    if order_number.startswith('A20'):
        return Group.objects.get(name='besart')
    elif order_number.startswith('AU'):
        return Group.objects.get(name='kasia')
    elif order_number.startswith('4DICH'):
        return Group.objects.get(name='4dich')
    else:
        return None


def create_order(line, request, owner):
    date_line = line[0].split('.')
    pub = date(day=int(date_line[0]), month=int(date_line[1]), year=int(date_line[2]))
    if len(line) == 5:
        if line[3].startswith('1'):
            order = ActiveOrder(order_number=line[1], order_status='1', pub_date=pub, image=line[2].replace('.jpg', ''),
                                divided='całe', owner=owner, tracking_number=line[4])
        elif line[3].startswith('2'):
            order = ActiveOrder(order_number=line[1], order_status='1', pub_date=pub, image=line[2].replace('.jpg', ''),
                                divided='połówka', owner=owner)
        else:
            order = ActiveOrder(order_number=line[1], order_status='1', pub_date=pub, image=line[2].replace('.jpg', ''),
                                owner=owner)
    elif len(line) == 4:
        if line[3].startswith('1'):
            order = ActiveOrder(order_number=line[1], order_status='1', pub_date=pub, image=line[2].replace('.jpg', ''),
                                divided='całe', owner=owner)
        elif line[3].startswith('2'):
            order = ActiveOrder(order_number=line[1], order_status='1', pub_date=pub, image=line[2].replace('.jpg', ''),
                                divided='połówka', owner=owner)
        else:
            order = ActiveOrder(order_number=line[1], order_status='1', pub_date=pub, image=line[2].replace('.jpg', ''),
                                owner=owner)
    elif len(line) == 3:
        if line[3].endswith('.jpg'):
            order = ActiveOrder(order_number=line[1], order_status='1', pub_date=pub, image=line[2].replace('.jpg', ''),
                                divided='brak', owner=owner)
        else:
            if line[2].startswith('1'):
                order = ActiveOrder(order_number=line[1], order_status='1', pub_date=pub, divided='całe', owner=owner)
            elif line[2].startswith('2'):
                order = ActiveOrder(order_number=line[1], order_status='1', pub_date=pub, divided='połówka',
                                    owner=owner)
            else:
                order = ActiveOrder(order_number=line[1], order_status='1', pub_date=pub, owner=owner)
    else:
        order = ActiveOrder(order_number=line[1], order_status='1',
                            pub_date=pub,
                            owner=owner)
    status = OrderStatusChange(order=order, change_owner=request.user,
                               previous_state='1', new_state='1')
    order.save()
    status.save()


def get_page(queryset, current_page, page_len):
    prev_page = current_page - 1
    if queryset.count() > current_page * page_len:
        next_page = current_page + 1
    else:
        next_page = 0
    return prev_page, next_page
