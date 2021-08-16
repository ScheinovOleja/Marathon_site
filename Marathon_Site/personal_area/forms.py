from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Users

#
# class CustomUserCreationForm(UserCreationForm):
#     class Meta(UserCreationForm):
#         model = Users
#         fields = ('username', 'email', 'sex')
#
#
# class CustomUserChangeForm(UserChangeForm):
#     class Meta:
#         model = Users
#         fields = ('username', 'email', 'sex')
#
#     # email = forms.EmailField()
#     sex = forms.CharField()
