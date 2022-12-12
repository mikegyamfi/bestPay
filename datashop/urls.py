from django.conf import settings
from django.urls import path
from . import views
from .mtn import mtn_bundle_views as bundle_views
from .airtelTigo import airtelTigo_bundle_views as tigo_bundle_views
from .voda import voda_bundle_views as voda_bundle_views
from .mtn import other_mtn_bundle_views as other_mtn_bundles
from .airtelTigo import sika_kokoo_views as sika_kokoo_bundles

urlpatterns = [
    path('airtime/mtn', views.mtn_request, name="mtn_airtime"),
    path('airtime/airtelTigo', views.airtel_tigo_request, name="tigo_airtime"),
    path('airtime/vodafone', views.voda_request, name="voda_airtime"),
    path('airtime/glo', views.glo_request, name="glo_airtime"),
    path('send_airtime_mtn/<str:client_ref>/<str:phone>/<str:amount>', views.send_airtime_mtn, name="send_airtime_mtn"),
    path('send_airtime_tigo/<str:client_ref>/<str:phone>/<str:amount>', views.send_airtime_tigo, name="send_airtime_tigo"),
    path('send_airtime_voda/<str:client_ref>/<str:phone>/<str:amount>', views.send_airtime_voda, name="send_airtime_voda"),
    path('send_airtime_glo/<str:client_ref>/<str:phone>/<str:amount>', views.send_airtime_glo, name="send_airtime_glo"),
    path('thank_you', views.thank_you, name="thank_you"),
    path('failed', views.failed, name="failed"),
    ###################################################################################################################
    path('bundle/mtn/0.5', bundle_views.pay_for_50p_bundle, name="mtn_50p_bundle"),
    path('send_0.5_mtn_bundle/<str:client_ref>/<str:phone_number>', bundle_views.send_50p_bundle, name="send_50p_bundle"),

    path('bundle/mtn/1', bundle_views.pay_for_1_bundle, name="mtn_1_bundle"),
    path('send_1_mtn_bundle/<str:client_ref>/<str:phone_number>', bundle_views.send_1_bundle, name="send_1_bundle"),

    path('bundle/mtn/3', bundle_views.pay_for_3_bundle, name="mtn_3_bundle"),
    path('send_3_mtn_bundle/<str:client_ref>/<str:phone_number>', bundle_views.send_3_bundle, name="send_3_bundle"),

    path('bundle/mtn/10', bundle_views.pay_for_10_bundle, name="mtn_10_bundle"),
    path('send_10_mtn_bundle/<str:client_ref>/<str:phone_number>', bundle_views.send_10_bundle, name="send_10_bundle"),

    path('bundle/mtn/20', bundle_views.pay_for_20_bundle, name="mtn_20_bundle"),
    path('send_20_mtn_bundle/<str:client_ref>/<str:phone_number>', bundle_views.send_20_bundle, name="send_20_bundle"),

    path('bundle/mtn/40', bundle_views.pay_for_40_bundle, name="mtn_40_bundle"),
    path('send_40_mtn_bundle/<str:client_ref>/<str:phone_number>', bundle_views.send_40_bundle, name="send_40_bundle"),

    path('bundle/mtn/60', bundle_views.pay_for_60_bundle, name="mtn_60_bundle"),
    path('send_60_mtn_bundle/<str:client_ref>/<str:phone_number>', bundle_views.send_60_bundle, name="send_60_bundle"),

    path('bundle/mtn/80', bundle_views.pay_for_80_bundle, name="mtn_80_bundle"),
    path('send_80_mtn_bundle/<str:client_ref>/<str:phone_number>', bundle_views.send_80_bundle, name="send_80_bundle"),

    path('bundle/mtn/100', bundle_views.pay_for_100_bundle, name="mtn_100_bundle"),
    path('send_100_mtn_bundle/<str:client_ref>/<str:phone_number>', bundle_views.send_100_bundle, name="send_100_bundle"),

    path('bundle/mtn/120', bundle_views.pay_for_120_bundle, name="mtn_120_bundle"),
    path('send_120_mtn_bundle/<str:client_ref>/<str:phone_number>', bundle_views.send_120_bundle, name="send_120_bundle"),

    path('bundle/mtn/150', bundle_views.pay_for_150_bundle, name="mtn_150_bundle"),
    path('send_150_mtn_bundle/<str:client_ref>/<str:phone_number>', bundle_views.send_150_bundle, name="send_150_bundle"),

    path('bundle/mtn/200', bundle_views.pay_for_200_bundle, name="mtn_200_bundle"),
    path('send_200_mtn_bundle/<str:client_ref>/<str:phone_number>', bundle_views.send_200_bundle, name="send_200_bundle"),

    path('bundle/mtn/250', bundle_views.pay_for_250_bundle, name="mtn_250_bundle"),
    path('send_250_mtn_bundle/<str:client_ref>/<str:phone_number>', bundle_views.send_250_bundle, name="send_250_bundle"),

    path('bundle/mtn/300', bundle_views.pay_for_300_bundle, name="mtn_300_bundle"),
    path('send_300_mtn_bundle/<str:client_ref>/<str:phone_number>', bundle_views.send_300_bundle, name="send_300_bundle"),

    path('bundle/mtn/400', bundle_views.pay_for_400_bundle, name="mtn_400_bundle"),
    path('send_400_mtn_bundle/<str:client_ref>/<str:phone_number>', bundle_views.send_400_bundle, name="send_400_bundle"),

    path('bundle/mtn/k1', bundle_views.pay_for_k1_bundle, name="mtn_k1_bundle"),
    path('send_k1_mtn_bundle/<str:client_ref>/<str:phone_number>', bundle_views.send_k1_bundle, name="send_k1_bundle"),

    path('bundle/mtn/vid1', other_mtn_bundles.pay_for_v1_bundle, name="mtn_v1_bundle"),
    path('send_v1_mtn_bundle/<str:client_ref>/<str:phone_number>', other_mtn_bundles.send_v1_bundle, name="send_v1_bundle"),

    path('bundle/mtn/vid5', other_mtn_bundles.pay_for_v5_bundle, name="mtn_v5_bundle"),
    path('send_v5_mtn_bundle/<str:client_ref>/<str:phone_number>', other_mtn_bundles.send_v5_bundle, name="send_v5_bundle"),

    path('bundle/mtn/vid10', other_mtn_bundles.pay_for_v10_bundle, name="mtn_v10_bundle"),
    path('send_v10_mtn_bundle/<str:client_ref>/<str:phone_number>', other_mtn_bundles.send_v10_bundle, name="send_v10_bundle"),

    path('bundle/mtn/social1', other_mtn_bundles.pay_for_s1_bundle, name="mtn_s1_bundle"),
    path('send_s1_mtn_bundle/<str:client_ref>/<str:phone_number>', other_mtn_bundles.send_s1_bundle, name="send_s1_bundle"),

    path('bundle/mtn/social5', other_mtn_bundles.pay_for_s5_bundle, name="mtn_s5_bundle"),
    path('send_s5_mtn_bundle/<str:client_ref>/<str:phone_number>', other_mtn_bundles.send_s5_bundle, name="send_s5_bundle"),

    path('bundle/mtn/social10', other_mtn_bundles.pay_for_s10_bundle, name="mtn_s10_bundle"),
    path('send_s10_mtn_bundle/<str:client_ref>/<str:phone_number>', other_mtn_bundles.send_s10_bundle, name="send_s10_bundle"),
    ####################################################################################################################

    path('bundle/tigo/1', tigo_bundle_views.pay_for_1_bundle, name="tigo_1_bundle"),
    path('send_1_tigo_bundle/<str:client_ref>/<str:phone_number>', tigo_bundle_views.send_1_bundle, name="send_1_bundle"),

    path('bundle/tigo/2', tigo_bundle_views.pay_for_2_bundle, name="tigo_2_bundle"),
    path('send_2_tigo_bundle/<str:client_ref>/<str:phone_number>', tigo_bundle_views.send_2_bundle, name="send_2_bundle"),

    path('bundle/tigo/5', tigo_bundle_views.pay_for_5_bundle, name="tigo_5_bundle"),
    path('send_5_tigo_bundle/<str:client_ref>/<str:phone_number>', tigo_bundle_views.send_5_bundle, name="send_5_bundle"),

    path('bundle/tigo/10', tigo_bundle_views.pay_for_10_bundle, name="tigo_10_bundle"),
    path('send_10_tigo_bundle/<str:client_ref>/<str:phone_number>', tigo_bundle_views.send_10_bundle, name="send_10_bundle"),

    path('bundle/tigo/20', tigo_bundle_views.pay_for_20_bundle, name="tigo_20_bundle"),
    path('send_20_tigo_bundle/<str:client_ref>/<str:phone_number>', tigo_bundle_views.send_20_bundle, name="send_20_bundle"),

    path('bundle/tigo/50', tigo_bundle_views.pay_for_50_bundle, name="tigo_50_bundle"),
    path('send_50_tigo_bundle/<str:client_ref>/<str:phone_number>', tigo_bundle_views.send_50_bundle, name="send_50_bundle"),

    path('bundle/tigo/100', tigo_bundle_views.pay_for_100_bundle, name="tigo_100_bundle"),
    path('send_100_tigo_bundle/<str:client_ref>/<str:phone_number>', tigo_bundle_views.send_100_bundle, name="send_100_bundle"),

    path('bundle/tigo/300', tigo_bundle_views.pay_for_300_bundle, name="tigo_300_bundle"),
    path('send_300_tigo_bundle/<str:client_ref>/<str:phone_number>', tigo_bundle_views.send_300_bundle, name="send_300_bundle"),

    path('bundle/tigo/350', tigo_bundle_views.pay_for_350_bundle, name="tigo_350_bundle"),
    path('send_350_tigo_bundle/<str:client_ref>/<str:phone_number>', tigo_bundle_views.send_350_bundle, name="send_350_bundle"),

    path('bundle/tigo/400', tigo_bundle_views.pay_for_400_bundle, name="tigo_400_bundle"),
    path('send_400_tigo_bundle/<str:client_ref>/<str:phone_number>', tigo_bundle_views.send_400_bundle, name="send_400_bundle"),

    path('bundle/tigo/sk3', sika_kokoo_bundles.pay_for_sk3_bundle, name="tigo_sk3_bundle"),
    path('send_sk3_tigo_bundle/<str:client_ref>/<str:phone_number>', sika_kokoo_bundles.send_sk3_bundle, name="send_sk3_bundle"),

    path('bundle/tigo/sk5', sika_kokoo_bundles.pay_for_sk5_bundle, name="tigo_sk5_bundle"),
    path('send_sk5_tigo_bundle/<str:client_ref>/<str:phone_number>', sika_kokoo_bundles.send_sk5_bundle, name="send_sk5_bundle"),
    
    path('bundle/tigo/sk6', sika_kokoo_bundles.pay_for_sk6_bundle, name="tigo_sk6_bundle"),
    path('send_sk6_tigo_bundle/<str:client_ref>/<str:phone_number>', sika_kokoo_bundles.send_sk6_bundle, name="send_sk6_bundle"),
    
    path('bundle/tigo/sk10', sika_kokoo_bundles.pay_for_sk10_bundle, name="tigo_sk10_bundle"),
    path('send_sk10_tigo_bundle/<str:client_ref>/<str:phone_number>', sika_kokoo_bundles.send_sk10_bundle, name="send_sk10_bundle"),
    
    path('bundle/tigo/sk11', sika_kokoo_bundles.pay_for_sk11_bundle, name="tigo_sk11_bundle"),
    path('send_sk11_tigo_bundle/<str:client_ref>/<str:phone_number>', sika_kokoo_bundles.send_sk11_bundle, name="send_sk11_bundle"),
    
    path('bundle/tigo/sk15', sika_kokoo_bundles.pay_for_sk15_bundle, name="tigo_sk15_bundle"),
    path('send_sk15_tigo_bundle/<str:client_ref>/<str:phone_number>', sika_kokoo_bundles.send_sk15_bundle, name="send_sk15_bundle"),

    path('bundle/tigo/sk20', sika_kokoo_bundles.pay_for_sk20_bundle, name="tigo_sk20_bundle"),
    path('send_sk20_tigo_bundle/<str:client_ref>/<str:phone_number>', sika_kokoo_bundles.send_sk20_bundle, name="send_sk20_bundle"),
    ##########################################################################################################################

    path('bundle/voda/0.5', voda_bundle_views.pay_for_50p_bundle, name="voda_50p_bundle"),
    path('send_50p_voda_bundle/<str:client_ref>/<str:phone_number>', voda_bundle_views.send_50p_bundle, name="send_50p_bundle"),

    path('bundle/voda/1', voda_bundle_views.pay_for_1_bundle, name="voda_1_bundle"),
    path('send_1_voda_bundle/<str:client_ref>/<str:phone_number>', voda_bundle_views.send_1_bundle, name="send_1_bundle"),

    path('bundle/voda/2', voda_bundle_views.pay_for_2_bundle, name="voda_2_bundle"),
    path('send_2_voda_bundle/<str:client_ref>/<str:phone_number>', voda_bundle_views.send_2_bundle, name="send_2_bundle"),

    path('bundle/voda/5', voda_bundle_views.pay_for_5_bundle, name="voda_5_bundle"),
    path('send_5_voda_bundle/<str:client_ref>/<str:phone_number>', voda_bundle_views.send_5_bundle, name="send_5_bundle"),

    path('bundle/voda/10', voda_bundle_views.pay_for_10_bundle, name="voda_10_bundle"),
    path('send_10_voda_bundle/<str:client_ref>/<str:phone_number>', voda_bundle_views.send_10_bundle, name="send_10_bundle"),

    path('bundle/voda/20', voda_bundle_views.pay_for_20_bundle, name="voda_20_bundle"),
    path('send_20_voda_bundle/<str:client_ref>/<str:phone_number>', voda_bundle_views.send_20_bundle, name="send_20_bundle"),

    path('bundle/voda/50', voda_bundle_views.pay_for_50_bundle, name="voda_50_bundle"),
    path('send_50_voda_bundle/<str:client_ref>/<str:phone_number>', voda_bundle_views.send_50_bundle, name="send_50_bundle"),

    path('bundle/voda/100', voda_bundle_views.pay_for_100_bundle, name="voda_100_bundle"),
    path('send_100_voda_bundle/<str:client_ref>/<str:phone_number>', voda_bundle_views.send_100_bundle, name="send_100_bundle"),

    path('bundle/voda/200', voda_bundle_views.pay_for_200_bundle, name="voda_200_bundle"),
    path('send_200_voda_bundle/<str:client_ref>/<str:phone_number>', voda_bundle_views.send_200_bundle, name="send_200_bundle"),

    path('bundle/voda/300', voda_bundle_views.pay_for_300_bundle, name="voda_300_bundle"),
    path('send_300_voda_bundle/<str:client_ref>/<str:phone_number>', voda_bundle_views.send_300_bundle, name="send_300_bundle"),

    path('bundle/voda/400', voda_bundle_views.pay_for_400_bundle, name="voda_400_bundle"),
    path('send_400_voda_bundle/<str:client_ref>/<str:phone_number>', voda_bundle_views.send_400_bundle, name="send_400_bundle"),
]