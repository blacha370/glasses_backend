from django import forms


class StatusForm(forms.Form):
    order_statuses = (('1', 'not recieved'),
                      ('2', 'recieved'),
                      ('3', 'in preparation'),
                      ('4', 'finished'),
                      ('5', 'send'),
                      ('6', 'done'))
    value = forms.ChoiceField(label='status', widget=forms.Select, choices=order_statuses)


class LoginForm(forms.Form):
    login = forms.CharField(label='Login:')
    password = forms.CharField(label='Password:', widget=forms.PasswordInput)
