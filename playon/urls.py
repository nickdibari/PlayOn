from django.conf.urls import url, include
from django.contrib import admin
from viewer import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^viewer/', views.landing),
    url(r'^', views.landing)
]
