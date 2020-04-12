from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('join', views.join, name="join"),
    path('game/<str:name>/', views.game, name="game"),
    path('game/<str:name>/say/<str:text>', views.say, name="say"),
]
