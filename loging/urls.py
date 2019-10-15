from django.conf.urls import url

from . import views
    
app_name = 'loging'

urlpatterns = [
    url(r'^register/$', views.UserCreateView.as_view(),
        name='register'),
    url(r'^login/$', views.UserLoginView.as_view(),
        name='login'),
    url(r'^logout/$', views.UserLogoutView.as_view(),
        name='logout')
]