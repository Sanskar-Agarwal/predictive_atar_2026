# myapp/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Invitation, CustomUser

class InvitationForm(forms.ModelForm):
    class Meta:
        model = Invitation
        fields = ['email']

class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']
