from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
class Event(models.Model):
  title = models.CharField(max_length=200)
  description = models.TextField(max_length=500)
  location = models.TextField(max_length=500)
  start_date = models.DateTimeField('Event Date')
  end_date = models.DateTimeField('Event End Date')
  created_date = models.DateTimeField(auto_now=True)
  updated_date = models.DateTimeField(auto_now=True)
  attendees_count = models.IntegerField()
  theme_colors = models.CharField(max_length=100)
  theme_images = models.ImageField(upload_to='events/%Y/%m/',
        blank=True,
        null=True)
  user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='events'
    )


  def __str__(self):
    return self.title

  def get_absolute_url(self):
    return reverse('event-details', kwargs={'pk': self.id})
  



  