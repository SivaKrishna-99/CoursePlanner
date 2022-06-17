from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('valid-pos', views.valid, name='valid_pos'),
    path('invalid-pos', views.summary, name='invalid_pos'),
    path('summary', views.summary, name='summary'),
    path('select-courses', views.select_courses, name='select_courses'),
    path('search_courses', views.search_courses, name='search_courses'),
    path('search_results', views.search_results, name='search_results'),
    path('search_detail/<str:course_name>', views.search_detail, name='search_detail'),
    path('about', views.about, name='about'),
    path('downloadPOS', views.downloadPOS, name='downloadPOS')
]