from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class User(models.Model):
  name = models.CharField(max_length=50)
  email = models.CharField()
  age = models.IntegerField()

  def __str__(self):
    return self.name

  def get_absolute_url(self):
      return reverse("user-details", kwargs={"pk": self.id})

# Create your models here.
class Event(models.Model):
  title = models.CharField(max_length=200)
  description = models.TextField(max_length=500)
  location = models.TextField(max_length=500)
  start_date = models.DateField('Event Date')
  end_date = models.DateField('Event End Date')
  created_date = models.DateTimeField(auto_now_add=True)
  updated_date = models.DateTimeField(auto_now_add=True)
  attendees_count = models.IntegerField()
  theme_colors = models.CharField(max_length=100)
  theme_images = models.ImageField(upload_to='events/%Y/%m/',
        blank=True,
        null=True)
  user = models.ForeignKey(User,on_delete=models.CASCADE)


  def __str__(self):
    return self.name

  def get_absolute_url(self):
      return reverse('event-details', kwargs={'event_id': self.id})
  



  