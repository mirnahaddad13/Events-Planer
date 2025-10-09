from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class CustomUserCreationForm(UserCreationForm):
    age = forms.IntegerField(required=True,label='Age')
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'age']
    def clean_age(self):
        age=self.cleaned_data.get('age')
        if age < 18:
            raise ValidationError('You must be at least 18 years old to sign up.')
        else:
            return age