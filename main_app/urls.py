from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name = 'login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('events/<int:event_id>/', views.event_details, name='event-details'),
   path('events/create/', views.EventCreate.as_view(), name='event-create'),
   path('events/<int:pk>/update/', views.EventUpdate.as_view(), name='event-update'),
   path('events/<int:pk>/delete/', views.EventDelete.as_view(), name='event-delete'),

 ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
