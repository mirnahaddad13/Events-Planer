from django.shortcuts import render,redirect 
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render,redirect
from .forms import CustomUserCreationForm, EventForm
from .models import Event
from datetime import timedelta
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.views.generic import DetailView
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect




User = get_user_model()
    
def home(request):
  return render(request,'home.html')

def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()                
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'signup.html', {'form': form})
class CustomLoginView(LoginView):
    template_name = 'login.html'

    # prevent logged-in users from accessing the login page
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

@login_required
def event_index(request):
  events = Event.objects.filter(user=request.user).order_by('start_date')
  return render(request, 'events/index.html', {'events': events})

class EventDetail(LoginRequiredMixin, DetailView):
    model = Event
    template_name = 'events/details.html'

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            # Admins can view all events
            return Event.objects.all()
        # Regular users only see their own events
        return Event.objects.filter(user=user)
    
class EventCreate(LoginRequiredMixin,CreateView):
  model = Event
  form_class = EventForm
  template_name = 'main_app/event_form.html'
  success_url = '/events/'
  def form_valid(self, form):
        now = timezone.now()
        start = form.cleaned_data.get('start_date')
        end = form.cleaned_data.get('end_date')

        # Must reserve at least 5 hours in advance
        if start and start < now + timedelta(hours=5):
            form.add_error('start_date', 'You must reserve at least 5 hours in advance.')

        # No past dates at all
        if start and start < now:
            form.add_error('start_date', 'Start date/time cannot be in the past.')
        if end and end < now:
            form.add_error('end_date', 'End date/time cannot be in the past.')

        # End must be after start
        if start and end and end <= start:
            form.add_error('end_date', 'End date/time must be after the start date/time.')

        if form.errors:
            return self.form_invalid(form)

        form.instance.user = self.request.user
        return super().form_valid(form)

class EventUpdate(LoginRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm

    def get_queryset(self):
        # Only allow the owner to edit
        return Event.objects.filter(user=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        event = self.get_object()
        # Block update if current event starts within 1 day
        if event.start_date < timezone.now() + timedelta(days=1):
            messages.error(request, 'You cannot edit this event less than 1 day before it starts.')
            return redirect('event-details', pk=event.pk)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        now = timezone.now()
        start = form.cleaned_data.get('start_date')
        end = form.cleaned_data.get('end_date')

        # No past dates
        if start and start < now:
            form.add_error('start_date', 'Start date/time cannot be in the past.')
        if end and end < now:
            form.add_error('end_date', 'End date/time cannot be in the past.')

        # Maintain the 1-day rule even for the new proposed start
        if start and start < now + timedelta(days=1):
            form.add_error('start_date', 'You cannot set the start time to less than 1 day from now.')

        # End must be after start
        if start and end and end <= start:
            form.add_error('end_date', 'End date/time must be after the start date/time.')

        if form.errors:
            return self.form_invalid(form)

        form.instance.user = self.request.user
        return super().form_valid(form)

class EventDelete(LoginRequiredMixin, DeleteView):
    model = Event
    success_url = '/events/'

    def get_queryset(self):
        # Only allow the owner to delete
        return Event.objects.filter(user=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        event = self.get_object()  # 404s if not owner
        # Block delete if event starts within 1 day
        if event.start_date < timezone.now() + timedelta(days=1):
            messages.error(request, 'You cannot delete this event less than 1 day before it starts.')
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)




