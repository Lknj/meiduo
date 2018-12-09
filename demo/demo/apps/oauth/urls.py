from django.conf.urls import url
from . import views

urlpatterns = [
    url('^qq/authorization/$', views.QQLoginURLView.as_view()),
    url('^qq/user/$', views.QQUserView.as_view()),

]
