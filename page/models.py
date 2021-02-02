from django.db import models
from django.utils import timezone, dateformat
from django.contrib.auth.models import User, Group


class ActiveOrder(models.Model):
    owner = models.ForeignKey(Group, on_delete=models.CASCADE, default=None)
    order_number = models.CharField(max_length=14, unique=True, default=None)
    pub_date = models.DateField(auto_now_add=True)
    order_statuses = [('1', 'Nowe'),
                      ('2', 'W przygotowaniu'),
                      ('3', 'Wysłane'),
                      ('4', 'Zakończone'),
                      ('5', 'Anulowane')]
    order_status = models.CharField(max_length=1, choices=order_statuses, default=order_statuses[0])
    image = models.CharField(max_length=20, default='?')
    divided = models.CharField(max_length=8, default='?')
    tracking_number = models.CharField(max_length=22, default='?')

    def __str__(self):
        return self.order_number

    def update_status(self, new_status=None):
        if new_status is None:
            self.order_status = self.order_statuses[self.order_statuses.index(self.order_status) + 1]
            if self.order_status == ('4', 'Zakończone'):
                self.complete_order()
                return None
            return True
        elif new_status in self.order_statuses:
            self.order_status = new_status
            self.save()
            if self.order_status == ('4', 'Zakończone'):
                self.complete_order()
                return None
            return True
        return False

    def complete_order(self):
        unactive = UnactiveOrder(order_number=self.order_number, pub_date=self.pub_date, image=self.image,
                                 owner=self.owner)
        unactive.save()
        self.delete()


class OrderStatusChange(models.Model):
    order = models.ForeignKey(ActiveOrder, on_delete=models.CASCADE)
    pub_date = models.DateField(auto_now_add=True)
    change_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    previous_state = models.CharField(max_length=1, choices=ActiveOrder.order_statuses)
    new_state = models.CharField(max_length=1, choices=ActiveOrder.order_statuses)


class UnactiveOrder(models.Model):
    owner = models.ForeignKey(Group, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=14, unique=True)
    pub_date = models.DateField()
    unactivation_date = models.DateField(auto_now_add=True)
    image = models.CharField(max_length=20, default='?')

    def __str__(self):
        return self.order_number


class MessagesThread(models.Model):
    subject = models.CharField(max_length=14, default=None)
    creator = models.ForeignKey(Group, default=None, on_delete=models.CASCADE,
                                related_name='creator')
    reciever = models.ForeignKey(Group, default=None, on_delete=models.CASCADE,
                                 related_name='reciever')

    def __str__(self):
        return self.subject

    def delete_thread(self):
        archive_thread = ArchiveThread(subject=self.subject)
        archive_thread.save()
        msgs = Message.objects.filter(thread=self.id)
        for msg in msgs:
            msg.delete_message(archive_thread)
        self.delete()


class Message(models.Model):
    thread = models.ForeignKey(MessagesThread, on_delete=models.CASCADE, default=None)
    message_op = models.CharField(max_length=20, default=None)
    message_text = models.CharField(max_length=200, default=None)
    message_date = models.CharField('date', default='09:03 25.09.20',
                                    max_length=16)

    def __str__(self):
        return self.thread.subject

    def delete_message(self, thread):
        archive_message = ArchiveMessage(thread=thread, message_op=self.message_op, message_text=self.message_text,
                                         message_date=self.message_date)
        archive_message.save()
        self.delete()


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    thread = models.ForeignKey(MessagesThread, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.thread.subject


class ArchiveThread(models.Model):
    subject = models.CharField(max_length=14, default=None)

    def __str__(self):
        return self.subject


class ArchiveMessage(models.Model):
    thread = models.ForeignKey(ArchiveThread, on_delete=models.CASCADE, default=None)
    message_op = models.CharField(max_length=20, default=None)
    message_text = models.CharField(max_length=200, default=None)
    message_date = models.CharField('date', default='09:03 25.09.20',
                                    max_length=16)

    def __str__(self):
        return self.thread.subject
