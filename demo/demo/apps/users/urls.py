from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token

from . import views
from rest_framework.routers import DefaultRouter

urlpatterns = [
    url(r'^usernames/(?P<username>\w{5,20})/count/$', views.UsernameCountView.as_view()),
    url(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', views.MobileCountView.as_view()),
    url(r'^users/$', views.UserRegisterView.as_view()),
    url(r'^authorizations/$', obtain_jwt_token),
    url('^user/$', views.UserView.as_view()),
    url('^emails/$', views.EmailView.as_view()),
    # url('^addresses/$', views.AddressView.as_view()),

]

router = DefaultRouter()
router.register('addresses', views.AddressesView, base_name='addresses')
urlpatterns += router.urls