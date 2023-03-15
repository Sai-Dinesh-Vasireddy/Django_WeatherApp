
from django.contrib import admin
from django.urls import path,include
from weather import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.login_signup,name='login'),
    path('weather',views.home, name='WeatherInfo'),
    path('delete/<CName>',views.delete_city,name='DelCity'),
    path('logout_user',views.logout_user,name='logout'),
]
