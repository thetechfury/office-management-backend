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
    Inventory_Manager = 'inventory_manager'


    """User model."""
    ROLE_CHOICES = (
        (ENDUSER,"End User"),
        (Accountant,"Accountant"),
        (MANAGER,"Manager"),
        (Inventory_Manager,'Inventory Manager'),
        (ADMIN,"Admin")
    )
    role = models.CharField(max_length=30,choices=ROLE_CHOICES,default=ROLE_CHOICES[0])
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class Team(models.Model):
    name = models.CharField(max_length=100)
    leader = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)

class Membership(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    team = models.ForeignKey(Team,on_delete=models.CASCADE,related_name='members')

    class Meta:
        unique_together = ('user', 'team')

    def __str__(self):
        return f'{str(self.user)}) in {str(self.team)}'




class Profile(models.Model):
    date_of_birth = models.DateField()
    bio = models.TextField(max_length=500)
    phone = models.CharField(max_length=13)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.user.email


class Education(models.Model):
    degree = models.CharField(max_length=50)
    total_marks = models.DecimalField(decimal_places=2,max_digits=6)
    obtain_marks = models.DecimalField(decimal_places=2,max_digits=6)
    start_date = models.DateField(auto_now=False)
    end_date = models.DateField(auto_now=False)
    institute = models.CharField(max_length=100)
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='educations')

    def __str__(self):
        return str(f'{self.degree} - {self.profile.user.email}')




class ProfileImage(models.Model):
    title = models.CharField(max_length=30)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    profile = models.OneToOneField(Profile,on_delete=models.CASCADE,related_name='profile_image')
    def __str__(self):
        return self.title

class Skills(models.Model):
    beigner = 'beigner'
    intermediate = 'intermediate'
    expert = 'expert'


    """User model."""
    LEVEL_CHOICES = (
        (beigner, "Beigner"),
        (intermediate, "Intermediate"),
        (expert, "expert"),

    )

    name = models.CharField(max_length=50)
    level = models.CharField(max_length=30,choices=LEVEL_CHOICES,default=beigner)
    description = models.CharField(max_length=300,null=True,blank=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='skills')

    def __str__(self):
        return str(f'{self.name} - {self.level}')

class WorkingExperience(models.Model):
    title = models.CharField(max_length=50)
    company_name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    joining_date = models.DateField()
    end_date = models.DateField()
    remarks = models.CharField(max_length=500)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='experience')

    def __str__(self):
        return f'{self.title} - {self.company_name} '




class Address(models.Model):
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='address')

    def __str__(self):
        return str(f'{self.name} - {self.level}')



# class Blog(models.Model):
#     name = models.CharField(max_length=100)
#     tagline = models.TextField()
#
#     def __str__(self):
#         return self.name
#
#
# class Author(models.Model):
#     name = models.CharField(max_length=200)
#     email = models.EmailField()
#
#     def __str__(self):
#         return self.name
#
#
# class Entry(models.Model):
#     blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
#     headline = models.CharField(max_length=255)
#     body_text = models.TextField()
#     pub_date = models.DateField()
#     mod_date = models.DateField(default=date.today)
#     authors = models.ManyToManyField(Author)
#     number_of_comments = models.IntegerField(default=0)
#     number_of_pingbacks = models.IntegerField(default=0)
#     rating = models.IntegerField(default=5)
#
#     def __str__(self):
#         return self.headline