from django.contrib import admin
from django.urls import path
from analytics import views
from users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.index, name='index'),
    path('full_info/', views.full_info, name='full_info'),
    path('demand/', views.demand, name='demand'),
    path('geography/', views.geography, name='geography'),
    path('top_skills', views.top_skills, name='top_skills'),
    path('last_vacancies/', views.last_vacancies, name='last_vacancies'),
    path('register/', user_views.register, name='register'),
    path('', user_views.authorise, name='authorise'),
]
