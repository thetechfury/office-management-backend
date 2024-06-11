from django.db import models
from django.contrib.auth.models import AbstractUser
from .custom_managers import CustomUserManager
from django.utils.translation import gettext_lazy as _

# Create your models here.



class User(AbstractUser):
    ENDUSER = 'enduser'
    ADMIN = 'admin'
    MANAGER = 'manager'
    Accountant = 'accountant'

    """User model."""
    ROLE_CHOICES = (
        (ENDUSER,"End User"),
        (Accountant,"Accountant"),
        (MANAGER,"Manager"),
        (ADMIN,"Admin")
    )
    role = models.CharField(max_length=30,choices=ROLE_CHOICES,default=ROLE_CHOICES[0])
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()



class Team(models.Model):
    name = models.CharField(max_length=100)
    leader = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)

class Membership(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    team = models.ForeignKey(Team,on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'team')

    def __str__(self):
        return f'{str(self.user)}) in {str(self.team)}'


