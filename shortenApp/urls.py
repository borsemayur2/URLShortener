from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('short_id', views.redirect_original, name='redirectoriginal'),
    path('makeshort', views.shorten_url, name='shortenurl'),
]
