from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Event 
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
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title','description','location','start_date','end_date','attendees_count','theme_colors','theme_images']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Event title'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Event description'}),
            'location': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Event location'}),
            'start_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',  
                'class': 'form-input'
            }),
            'end_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local', 
                'class': 'form-input'
            }),
            'attendees_count': forms.NumberInput(attrs={'class': 'form-input', 'min': 0}),
            'theme_colors': forms.TextInput(attrs={'class': 'form-input'}),
            'theme_images': forms.ClearableFileInput(attrs={'class': 'form-input'}),
        }