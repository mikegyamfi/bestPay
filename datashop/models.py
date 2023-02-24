from django.db import models

# Create your models here.
class AppPayment(models.Model):
    username = models.CharField(max_length=256, null=False, blank=False)
    reference = models.CharField(max_length=256, null=False, blank=False)
    payment_number = models.CharField(max_length=256, null=True, blank=True)
    amount = models.FloatField(null=True, blank=True)
    payment_description = models.CharField(max_length=500, null=True, blank=True)
    transaction_status = models.CharField(max_length=256, null=True, blank=True)
    transaction_date = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=500, null=True, blank=True)
    payment_visited = models.BooleanField(blank=False, null=False)

    def __str__(self):
        return f"{self.username} - {self.payment_number} - {self.reference}"


class AirtimeTransaction(models.Model):
    username = models.CharField(max_length=256, null=False, blank=False)
    email = models.EmailField(max_length=250, null=False, blank=True)
    airtime_number = models.PositiveBigIntegerField(null=False, blank=False)
    airtime_amount = models.FloatField(null=False, blank=True)
    provider = models.CharField(max_length=20, null=False, blank=True)
    reference = models.CharField(max_length=20, null=False, blank=True)
    transaction_date = models.DateTimeField(auto_now_add=True)
    transaction_status = models.CharField(max_length=100, null=False)

    def __str__(self):
        return f"{self.username} - {self.airtime_number} - {self.reference}"


class MTNBundleTransaction(models.Model):
    username = models.CharField(max_length=256, null=False, blank=False)
    email = models.EmailField(max_length=250, null=False, blank=True)
    bundle_number = models.PositiveBigIntegerField(null=False, blank=False)
    offer = models.CharField(max_length=250, null=False, blank=False)
    reference = models.CharField(max_length=20, null=False, blank=True)
    transaction_date = models.DateTimeField(auto_now_add=True)
    transaction_status = models.CharField(max_length=100, null=False)

    def __str__(self):
        return f"{self.username} - {self.bundle_number} - {self.reference}"


class OtherMTNBundleTransaction(models.Model):
    username = models.CharField(max_length=256, null=False, blank=False)
    email = models.EmailField(max_length=250, null=False, blank=True)
    bundle_number = models.PositiveBigIntegerField(null=False, blank=False)
    offer = models.CharField(max_length=250, null=False, blank=False)
    reference = models.CharField(max_length=20, null=False, blank=True)
    transaction_date = models.DateTimeField(auto_now_add=True)
    transaction_status = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f"{self.username} - {self.bundle_number} - {self.reference}"


class VodafoneBundleTransaction(models.Model):
    username = models.CharField(max_length=256, null=False, blank=False)
    email = models.EmailField(max_length=250, null=False, blank=True)
    bundle_number = models.PositiveBigIntegerField(null=False, blank=False)
    offer = models.CharField(max_length=250, null=False, blank=False)
    reference = models.CharField(max_length=20, null=False, blank=True)
    transaction_date = models.DateTimeField(auto_now_add=True)
    transaction_status = models.CharField(max_length=100, null=False)

    def __str__(self):
        return f"{self.username} - {self.bundle_number} - {self.reference}"


class AirtelTigoBundleTransaction(models.Model):
    username = models.CharField(max_length=256, null=False, blank=False)
    email = models.EmailField(max_length=250, null=False, blank=True)
    bundle_number = models.PositiveBigIntegerField(null=False, blank=False)
    offer = models.CharField(max_length=250, null=False, blank=False)
    reference = models.CharField(max_length=20, null=False, blank=True)
    transaction_date = models.DateTimeField(auto_now_add=True)
    transaction_status = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f"{self.username} - {self.bundle_number} - {self.reference}"


class SikaKokooBundleTransaction(models.Model):
    username = models.CharField(max_length=256, null=False, blank=False)
    email = models.EmailField(max_length=250, null=False, blank=True)
    bundle_number = models.PositiveBigIntegerField(null=False, blank=False)
    offer = models.CharField(max_length=250, null=False, blank=False)
    reference = models.CharField(max_length=20, null=False, blank=True)
    transaction_date = models.DateTimeField(auto_now_add=True)
    transaction_status = models.CharField(max_length=100, null=False)

    def __str__(self):
        return f"{self.username} - {self.bundle_number} - {self.reference}"


class TvTransaction(models.Model):
    username = models.CharField(max_length=256, null=False, blank=False)
    email = models.EmailField(max_length=250, null=False, blank=True)
    account_number = models.PositiveIntegerField(null=False, blank=False)
    amount = models.PositiveIntegerField(null=False, blank=False)
    provider = models.CharField(max_length=250, null=False, blank=False)
    reference = models.CharField(max_length=20, null=False, blank=True)
    transaction_date = models.DateTimeField(auto_now_add=True)
    transaction_status = models.CharField(max_length=100, null=False)

    def __str__(self):
        return f"{self.username} - {self.account_number} - {self.reference}"


class AppIShareBundleTransaction(models.Model):
    username = models.CharField(max_length=250, null=False, blank=False)
    email = models.EmailField(max_length=250, null=False, blank=True)
    bundle_number = models.BigIntegerField(null=False, blank=False)
    offer = models.CharField(max_length=250, null=False, blank=False)
    batch_id = models.CharField(max_length=250, null=False, blank=False)
    message = models.CharField(max_length=250, null=True, blank=True)
    reference = models.CharField(max_length=20, null=False, blank=True)
    transaction_date = models.DateTimeField(auto_now_add=True)
    transaction_status = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f"{self.username} - {self.bundle_number} - {self.reference}"


class Intruder(models.Model):
    username = models.CharField(max_length=256, null=False, blank=False)
    reference = models.CharField(max_length=256, null=False, blank=False)
    transaction_date = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}"                 