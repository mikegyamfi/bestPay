from django.shortcuts import render
from datashop import models


def airtime_transactions(request, username):
    all_airtime_transactions = models.AirtimeTransaction.objects.filter(username=username)
    context = {'txns': all_airtime_transactions, 'heading': "Airtime Transactions"}
    return render(request, "history_table.html", context=context)


def voda_bundle_transactions(request, username):
    all_voda_bundle_transactions = models.VodafoneBundleTransaction.objects.filter(username=username)
    context = {'txns': all_voda_bundle_transactions, 'heading': "Vodafone Bundle Transactions"}
    return render(request, "bundle_table.html", context=context)


def mtn_bundle_transactions(request, username):
    all_mtn_bundle_transactions = models.MTNBundleTransaction.objects.filter(username=username)
    context = {'txns': all_mtn_bundle_transactions, 'heading': "MTN Bundle Transactions"}
    return render(request, "bundle_table.html", context=context)


def tigo_bundle_transactions(request, username):
    all_tigo_bundle_transactions = models.AirtelTigoBundleTransaction.objects.filter(username=username)
    context = {'txns': all_tigo_bundle_transactions, 'heading': "AirtelTigo Bundle Transactions"}
    return render(request, "bundle_table.html", context=context)


def other_mtn_bundle_transactions(request, username):
    all_other_mtn_bundle_transactions = models.AirtimeTransaction.objects.filter(username=username)
    context = {'txns': all_other_mtn_bundle_transactions, 'heading': "Other MTN Bundle Transactions"}
    return render(request, "bundle_table.html", context=context)


def sika_kokoo_bundle_transactions(request, username):
    all_sika_kokoo_transactions = models.SikaKokooBundleTransaction.objects.filter(username=username)
    context = {'txns': all_sika_kokoo_transactions, 'heading': "Sika Kokoo Bundle Transactions"}
    return render(request, "bundle_table.html", context=context)


def ishare_bundle_transactions(request, username):
    all_ishare_transactions = models.SikaKokooBundleTransaction.objects.filter(username=username)
    print(all_ishare_transactions[0])
    context = {'txns': all_ishare_transactions, 'heading': "Flexi Bundle Transactions"}
    return render(request, "ishare_table.html", context=context)


def tv_transactions(request, username):
    all_tv_transactions = models.SikaKokooBundleTransaction.objects.filter(username=username)
    context = {'txns': all_tv_transactions, 'heading': "TV Transactions"}
    return render(request, "tv_table.html", context=context)

