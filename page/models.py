from django.db import models
from django.utils import timezone, dateformat


class ActiveOrder(models.Model):
    order_number = models.CharField(max_length=14)
    pub_date = models.CharField(max_length=10)
    order_statuses = [('1', 'not recieved'),
                      ('2', 'recieved'),
                      ('3', 'in preparation'),
                      ('4', 'finished'),
                      ('5', 'send'),
                      ('6', 'done')]
    order_status = models.CharField(max_length=1, choices=order_statuses, default=order_statuses[0])

    def __str__(self):
        return self.order_number

    def __del__(self):
        if self.order_status == '6':
            unactive = UnactiveOrder(order_number=self.order_number, pub_date=self.pub_date)
            unactive.save()
            self.delete()


class OrderStatusChange(models.Model):
    order = models.ForeignKey(ActiveOrder, on_delete=models.CASCADE)
    date = models.CharField('date', default=dateformat.format(timezone.now(), 'H:i d.m.y'),
                            max_length=16)
    change_owner = models.CharField(max_length=20)
    previous_state = models.CharField(max_length=1, choices=ActiveOrder.order_statuses)
    new_state = models.CharField(max_length=1, choices=ActiveOrder.order_statuses)


class UnactiveOrder(models.Model):
    order_number = order_number = models.CharField(max_length=14)
    pub_date = models.CharField(max_length=10)
    unactivation_date = models.CharField('date_deleted', default=dateformat.format(timezone.now(), 'd.m.y'),
                                         max_length=10)
    order_status = models.CharField(max_length=1, default='6')

    def __str__(self):
        return self.order_number


class MessagesThread(models.Model):
    subject = models.CharField(max_length=14)

    def __str__(self):
        return self.subject


class Message(models.Model):
    thread = models.ForeignKey(MessagesThread, on_delete=models.CASCADE)
    message_op = models.CharField(max_length=20)
    message_text = models.CharField(max_length=200)
    message_date = models.CharField('date', default=dateformat.format(timezone.now(), 'H:i d.m.y'),
                                    max_length=16)

    def __str__(self):
        return self.thread.subject
