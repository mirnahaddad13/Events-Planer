from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    age = forms.IntegerField(
        required=True,
        label='Age',
        min_value=0,
        help_text="You must be at least 18 years old to sign up.",
        widget=forms.NumberInput(attrs={
            'inputmode': 'numeric',
            'autocomplete': 'off',
            'min':0
        })
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'age']

    def clean_age(self):
        cleaned_data = super().clean()
        age = cleaned_data.get('age')

        if age is None or age < 18:
            # Add a non-field error instead of a field error
            self.add_error(None, ValidationError("Form is invalid. Please read the rule carefully."))
