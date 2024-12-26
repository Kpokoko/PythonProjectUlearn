from django.contrib import admin
from django.urls import path
from analytics import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', views.index, name='index'),
    path('general_statistics/', views.general_statistics, name='general_statistics'),
]
