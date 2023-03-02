from django.shortcuts import render
from datashop import models


def airtime_transactions(request, username):
    all_airtime_transactions = models.AirtimeTransaction.objects.filter(username=username)
    context = {'airtime_txns': all_airtime_transactions, 'heading': "Airtime Transactions"}
    return render(request, "history_table.html", context=context)

