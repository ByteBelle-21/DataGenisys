from django.urls import path
from . import views

urlpatterns = [
    path(route='',view=views.home_page,name='home_page'),
    path(route='aboutUs/',view=views.about_us,name='about_us_page'),
    path(route='form/',view=views.get_form,name='upload_file_page'),
]