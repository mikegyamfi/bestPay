from django.conf import settings
from django.urls import path
from . import views
from .mtn import mtn_bundle_views as bundle_views

urlpatterns = [
    path('airtime/mtn', views.mtn_request, name="mtn_airtime"),
    path('airtime/airtelTigo', views.airtel_tigo_request, name="tigo_airtime"),
    path('airtime/vodafone', views.voda_request, name="voda_airtime"),
    path('send_airtime_mtn/<str:client_ref>/<str:phone>/<str:amount>', views.send_airtime_mtn, name="send_airtime_mtn"),
    path('send_airtime_tigo/<str:client_ref>/<str:phone>/<str:amount>', views.send_airtime_tigo, name="send_airtime_tigo"),
    path('send_airtime_voda/<str:client_ref>/<str:phone>/<str:amount>', views.send_airtime_voda, name="send_airtime_voda"),
    path('thank_you', views.thank_you, name="thank_you"),
    path('failed', views.failed, name="failed"),

    path('bundle/mtn/0.5', bundle_views.pay_for_50p_bundle, name="mtn_50p_bundle"),
    path('send_50_mtn_bundle/<str:client_ref>/<str:phone_number>', bundle_views.send_50p_bundle, name="send_50p_bundle")
]