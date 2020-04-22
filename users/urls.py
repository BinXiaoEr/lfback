from django.conf.urls import url, include
from users.views import mylogin,mylogout,myregister

urlpatterns = [
    url('^login/', mylogin),
    url('^logout/',mylogout),
    url('^register/',myregister)
]
