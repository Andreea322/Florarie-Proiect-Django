from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name="acasa"),
    path('info',views.info, name="info",),
    path('exemplu_template',views.exemplu_template,name="exemplu_template"),
    path('exemplu_template2', views.exemplu_template2,name="exemplu_template2"),
    path('log',views.log, name="log"),
    path('istoric',views.istoric, name="istoric"),
    path('despre',views.despre, name="despre"),
    re_path(r'^accesare/(?P<id>\d+)/$', views.accesare),
    path('produse/', views.in_lucru, name='produse'),
    path('contact/', views.in_lucru, name='contact'),
    path('cos/', views.in_lucru, name='cos_virtual'),
    #path('contact',views.contact_view, name="contact"),
    ]