from django.urls import path
from django.conf.urls import url
from . import views
from django.conf import settings

urlpatterns = [
    path("", views.home),
    path("profile/", views.profile),
    path("business/", views.business),
    path('profile/update/', views.update_profile, name='update.profile'),
    path('add_business/', views.add_business, name='add_business'),
    path('add_post/', views.add_post, name='add_post'),
    path('search/', views.search, name='search.post'),
]