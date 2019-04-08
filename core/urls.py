from django.urls import path
from .views import *

core_urlpatterns = ([
    path('', IndexPageView.as_view(), name="home"),
    path('panel/', IndexPagePanelView.as_view(), name="panel"),
    path('prohibido',ProhibidoView.as_view(),name="prohibido"),
    path('notifications',Notification.as_view(),name="notification")


],"core")

