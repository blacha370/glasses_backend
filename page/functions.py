from .models import ActiveOrder, UnactiveOrder, OrderStatusChange
from django.utils import timezone, dateformat


def iterate_order_add(f, request):
    active_orders = set()
    for order in ActiveOrder.objects.all():
        active_orders.add(order.order_number)
    for order in UnactiveOrder.objects.all():
        active_orders.add(order.order_number)
    first = True
    for row in f:
        if first:
            first = False
            continue
        line = str(row)
        line = line[2:-5]
        if line == ';':
            continue
        elif ';' in line:
            line = line.split(';')
            if not line[1] in active_orders:
                order = ActiveOrder(order_number=line[1], order_status='1', pub_date=line[0])
                status = OrderStatusChange(order=order, change_owner=request.user.username,
                                           previous_state='1', new_state='1',
                                           date=dateformat.format(timezone.now(), 'H:i d.m.y'))
                order.save()
                status.save()
            else:
                continue
