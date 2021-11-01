from django.urls import path
from django.conf.urls import url
from . import views
from django.conf import settings

urlpatterns = [
    path("", views.home),
    # path("profile/", views.profile),
    # path('profile/update/', views.update_profile, name='update.profile'),
    # path('add/', views.postimage, name='save.project'),
    # path('display/<int:id>/', views.show_image, name='display.project'),
    # path("display/delete/<int:id>/", views.delete_project, name="delete.project"),
    # path('display/rate/<int:id>/', views.rating, name='rate.project'),
    # path('search/', views.search_post, name='search.post'),
]