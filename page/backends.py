from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def users_in_group1(self):
        return self.filter(groups__name='group1')
