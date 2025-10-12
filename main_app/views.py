from django.shortcuts import render,redirect 
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render,redirect
from .forms import CustomUserCreationForm
from .models import Event,User
from datetime import timedelta
from django.utils import timezone
from django.contrib import messages




def home(request):
  return render(request,'home.html')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()                
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'signup.html', {'form': form})

@login_required
def event_index(request):
  events = Event.objects.filter(user=request.user)
  return render(request, 'events/index.html', {'events': events})

@login_required
def event_details(request, cat_id):
  event = Event.objects.get(id=cat_id)
  user_dosent_have_events = User.objects.exclude(id__in=event.user.all().values_list('id'))

  return render(request, 'events/details.html', {
    'event': event,
    'user':user_dosent_have_events
  })

class EventCreate(LoginRequiredMixin,CreateView):
  model = Event
  fields = ['title','description','location','start_date','end_date','attendees_count','theme_colors','theme_images']
  def form_valid(self, form):
    start = form.cleaned_data.get('start_date')
    if start and start < timezone.now() + timedelta(hours=5):
        form.add_error('start_date', 'You must reserve at least 5 hours in advance.')
        return self.form_invalid(form)
    form.instance.user = self.request.user
    return super().form_valid(form)

class EventUpdate(LoginRequiredMixin, UpdateView):
    model = Event
    fields = ['title','description','location','start_date','end_date','attendees_count','theme_colors','theme_images']
    def get_queryset(self):
        # Only allow the owner to edit
        return Event.objects.filter(user=self.request.user)
    def dispatch(self, request, *args, **kwargs):
        event = self.get_object()
        # Block update if event starts within 1 day
        if event.start_date - timezone.now() < timedelta(days=1):
            messages.error(request, 'You cannot edit this event less than 1 day before it starts.')
            return redirect('event_details', pk=event.pk)
        return super().dispatch(request, *args, **kwargs)
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class EventDelete(LoginRequiredMixin, DeleteView):
    model = Event
    success_url = '/home'
    def get_queryset(self):
        # Only allow the owner to delete
        return Event.objects.filter(user=self.request.user)
    def dispatch(self, request, *args, **kwargs):
        event = self.get_object()
        # Block delete if event starts within 1 day
        if event.start_date - timezone.now() < timedelta(days=1):
            messages.error(request, 'You cannot delete this event less than 1 day before it starts.')
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)




