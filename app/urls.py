from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^query$', views.query, name='query'),
    url(r'^init$', views.init, name='init'),
    url(r'^next$', views.next, name='next'),
]
