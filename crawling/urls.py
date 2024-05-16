from django.urls import path, include

from . import views

app_name = 'crawling'

urlpatterns = [

    path('crawling/', views.crawling, name='crawling'),
    path('crawlingsubject/', views.crawlingsubject, name='crawlingsubject'),

]
