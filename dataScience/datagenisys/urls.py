from django.urls import path
from . import views

urlpatterns = [
    path(route='',view=views.get_dataset,name='get_dataset'),
    path('graphs/',view=views.get_graphs, name='get_graphs'),
    path('model/',view=views.get_prediction, name='get_prediction'),
]