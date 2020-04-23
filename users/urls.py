from django.conf.urls import url, include
from users.views import mylogin,mylogout,myregister,add_history

urlpatterns = [
    url('^login/', mylogin),
    url('^logout/',mylogout),
    url('^register/',myregister),
    url('^history/',add_history)
]
