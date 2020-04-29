from django.conf.urls import url, include
from users.views import mylogin,mylogout,myregister,add_history,get_recommend

urlpatterns = [
    url('^login/', mylogin),
    url('^logout/',mylogout),
    url('^register/',myregister),
    url('^history/',add_history),
    url('^performance',get_recommend)
]
