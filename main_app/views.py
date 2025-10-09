from django.shortcuts import render,redirect 
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render,redirect
from .forms import CustomUserCreationForm


def home(request):
  return render(request,'home.html')

def signup(request):
  error_message = ''

  if request.method == 'POST':
    # We need to create a `user` from the FORM Object
    # This FORM Object should include the data from the browser
    form = CustomUserCreationForm(request.POST)

    if form.is_valid():
      # If the form data is valid
      # then let's save it to the DB
      user = form.save()

      # Let's login the user after creating them
      login(request, user)

      # Let's send the user somewhere
      return redirect('home')
  else:
    error_message = 'Invalid sign up - try again!'

  # For a GET Request and also for a bad POST Request
  # Let's render the signup.html page with an empty form
  form = CustomUserCreationForm()
  return render(
    request,
    'signup.html',
    { 'form': form, 'error_message': error_message }
  )