from django.contrib.auth.forms import UserChangeForm,UserCreationForm
from .models import User
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = '__all__'
        exclude = ['username']


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = '__all__'
        exclude = ['username']
