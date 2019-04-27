from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('<str:short_id>', views.redirect_original, name='redirectoriginal'),
    path('makeshort/', views.shorten_url, name='shortenurl'),
    #re_path(r'^(?P&lt;short_id&gt;\w{6})$',views.redirect_original, name='redirectoriginal'),

]
