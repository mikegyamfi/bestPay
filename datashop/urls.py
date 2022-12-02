from django.conf import settings
from django.urls import path
from . import views

urlpatterns = [
    path('airtime/mtn', views.mtn_request, name="mtn_airtime"),
    path('airtime/airtelTigo', views.airtel_tigo_request, name="tigo_airtime"),
    path('airtime/vodafone', views.voda_request, name="voda_airtime")
]