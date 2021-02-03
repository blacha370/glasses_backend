from django.db import models
from django.contrib.auth.models import User, Group


class ActiveOrder(models.Model):
    owner = models.ForeignKey(Group, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=14, unique=True, default=None)
    pub_date = models.DateField()
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
            if self.order_status == '4':
                return None
            self.order_status = self.order_statuses[int(self.order_status)][0]
            return True
        elif new_status in '12345':
            if self.order_status == '4':
                return None
            self.order_status = new_status
            self.save()
            print(self.order_status)
            return True
        return False


class OrderStatusChange(models.Model):
    order = models.ForeignKey(ActiveOrder, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    change_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    previous_state = models.CharField(max_length=1, choices=ActiveOrder.order_statuses)
    new_state = models.CharField(max_length=1, choices=ActiveOrder.order_statuses)


class MessagesThread(models.Model):
    subject = models.CharField(max_length=14, default=None)
    groups = models.ManyToManyField(Group)
    archive = models.BooleanField(default=False)

    def __str__(self):
        return self.subject

    def delete_thread(self):
        self.archive = True
        messages = Message.objects.filter(thread=self)
        for message in messages:
            message.delete_message()
        self.save()


class Message(models.Model):
    thread = models.ForeignKey(MessagesThread, on_delete=models.CASCADE, default=None)
    message_op = models.ForeignKey(User, on_delete=models.CASCADE)
    message_text = models.CharField(max_length=200, default=None)
    message_date = models.DateTimeField(auto_now_add=True)
    archive = models.BooleanField(default=False)

    def __str__(self):
        return self.thread.subject

    def delete_message(self):
        self.archive = True
        self.save()


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    thread = models.ForeignKey(MessagesThread, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.thread.subject

    @classmethod
    def add_notification(cls, user: User, thread: MessagesThread):
        if not isinstance(user, User) or not isinstance(thread, MessagesThread):
            pass
        elif user.groups.all().intersection(thread.groups.all()):
            try:
                notification = Notification.objects.get(user=user, thread=thread)
                return notification
            except Notification.DoesNotExist:
                notification = Notification(user=user, thread=thread)
                notification.save()
                return notification
        return None
