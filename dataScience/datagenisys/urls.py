from django.urls import path
from . import views

urlpatterns = [
    path(route='',view=views.home_page,name='home_page'),
    path(route='aboutUs/',view=views.about_us,name='about_us_page'),
    path(route='upload/',view=views.get_dataset,name='get_dataset'),

]