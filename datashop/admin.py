from django.contrib import admin
from . import models


class AppPaymentAdmin(admin.ModelAdmin):
    list_display = ['username', 'payment_number', 'amount', 'reference', 'transaction_status', 'transaction_date']
    search_fields = ['reference']


class AirtelTigoBundleTransactionAdmin(admin.ModelAdmin):
    ...


class AirtimeTransactionAdmin(admin.ModelAdmin):
    ...


class AppIShareBundleTransactionAdmin(admin.ModelAdmin):
    ...


class MTNBundleTransactionAdmin(admin.ModelAdmin):
    ...


class VodafoneBundleTransactionAdmin(admin.ModelAdmin):
    ...


class OtherMTNBundleTransactionAdmin(admin.ModelAdmin):
    ...


class SikaKokooBundleTransactionAdmin(admin.ModelAdmin):
    ...


class TvTransactionAdmin(admin.ModelAdmin):
    ...


class IntruderAdmin(admin.ModelAdmin):
    ...


# Register your models here.
admin.site.register(models.AppPayment, AppPaymentAdmin)
admin.site.register(models.AirtelTigoBundleTransaction, AirtelTigoBundleTransactionAdmin)
admin.site.register(models.AirtimeTransaction, AirtimeTransactionAdmin)
admin.site.register(models.AppIShareBundleTransaction, AppIShareBundleTransactionAdmin)
admin.site.register(models.MTNBundleTransaction, MTNBundleTransactionAdmin)
admin.site.register(models.VodafoneBundleTransaction, VodafoneBundleTransactionAdmin)
admin.site.register(models.OtherMTNBundleTransaction, OtherMTNBundleTransactionAdmin)
admin.site.register(models.SikaKokooBundleTransaction, SikaKokooBundleTransactionAdmin)
admin.site.register(models.TvTransaction, TvTransactionAdmin)
admin.site.register(models.Intruder, IntruderAdmin)



