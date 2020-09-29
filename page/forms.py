from django import forms
from .models import ActiveOrder
from django.contrib.auth.models import Group


class StatusForm(forms.Form):
    order_statuses = ActiveOrder.order_statuses
    value = forms.ChoiceField(label='', widget=forms.Select, choices=order_statuses)


class LoginForm(forms.Form):
    login = forms.CharField(label='Login')
    password = forms.CharField(label='Hasło', widget=forms.PasswordInput)


class AddOrderForm(forms.Form):
    file = forms.FileField()


class AddMessageForm(forms.Form):
    message_text = forms.CharField(max_length=200, widget=forms.Textarea(attrs={'cols': 40, 'rows': 6}),
                                   label="Nowa wiadomość")


class AddMessageExtForm(forms.Form):
    choices = Group.objects.exclude(name='prod_admin').values_list()
    reciever = forms.ChoiceField(label='', widget=forms.Select, choices=choices)
    message_subject = forms.CharField(max_length=20, label='Temat')
    message_text = forms.CharField(max_length=200, widget=forms.Textarea, label="Wiadomość")
