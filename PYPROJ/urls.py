from django.contrib import admin
from django.urls import path
from analytics import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', views.index, name='index'),
    path('demand/', views.demand, name='demand'),
    path('geography/', views.geography, name='geography'),
    path('last_vacancies/', views.last_vacancies, name='last_vacancies')
]
