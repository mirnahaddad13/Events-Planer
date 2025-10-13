from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
     path('accounts/login/', views.CustomLoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('events/', views.event_index, name='my-events'),
    path('events/<int:pk>/', views.EventDetail.as_view(), name='event-details'),
     # this by default will go templates/main_app/event_form.html
    path('events/create/', views.EventCreate.as_view(), name='event-create'),
    path('events/<int:pk>/update/', views.EventUpdate.as_view(), name='event-update'),
    path('events/<int:pk>/delete/', views.EventDelete.as_view(), name='event-delete'),
    path('client-events/', views.client_events, name='client-events'),
 ]

#only serves uploaded media files (like user images) during development.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
