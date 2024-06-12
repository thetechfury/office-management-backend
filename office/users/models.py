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




class Profile(models.Model):
    date_of_birth = models.DateField()
    bio = models.TextField(max_length=500)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.user.email


class Education(models.Model):
    degree = models.CharField(max_length=50)
    total_marks = models.DecimalField(decimal_places=2,max_digits=6)
    obtain_marks = models.DecimalField(decimal_places=2,max_digits=6)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    institute = models.CharField(max_length=100)
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='educations')

    def __str__(self):
        return str(f'{self.degree} - {self.profile.user.email}')




class ProfileImage(models.Model):
    title = models.CharField(max_length=30)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    profile = models.OneToOneField(Profile,on_delete=models.CASCADE)
    def __str__(self):
        return self.title

