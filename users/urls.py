from django.conf.urls import url, include
from users.views import mylogin

urlpatterns = [
    url('^login/', mylogin)
]
