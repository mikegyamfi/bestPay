# Generated by Django 4.1.3 on 2023-02-23 02:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AirtelTigoBundleTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=256)),
                ('email', models.EmailField(blank=True, max_length=250)),
                ('bundle_number', models.PositiveBigIntegerField()),
                ('offer', models.CharField(max_length=250)),
                ('reference', models.CharField(blank=True, max_length=20)),
                ('transaction_date', models.DateTimeField(auto_now_add=True)),
                ('transaction_status', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AirtimeTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=256)),
                ('email', models.EmailField(blank=True, max_length=250)),
                ('airtime_number', models.PositiveBigIntegerField()),
                ('airtime_amount', models.FloatField(blank=True)),
                ('provider', models.CharField(blank=True, max_length=20)),
                ('reference', models.CharField(blank=True, max_length=20)),
                ('transaction_date', models.DateTimeField(auto_now_add=True)),
                ('transaction_status', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='AppIShareBundleTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=250)),
                ('email', models.EmailField(blank=True, max_length=250)),
                ('bundle_number', models.BigIntegerField()),
                ('offer', models.CharField(max_length=250)),
                ('batch_id', models.CharField(max_length=250)),
                ('message', models.CharField(blank=True, max_length=250, null=True)),
                ('reference', models.CharField(blank=True, max_length=20)),
                ('transaction_date', models.DateTimeField(auto_now_add=True)),
                ('transaction_status', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AppPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=256)),
                ('reference', models.CharField(max_length=256)),
                ('payment_number', models.CharField(blank=True, max_length=256, null=True)),
                ('amount', models.FloatField(blank=True, null=True)),
                ('payment_description', models.CharField(blank=True, max_length=500, null=True)),
                ('transaction_status', models.CharField(blank=True, max_length=256, null=True)),
                ('transaction_date', models.DateTimeField(auto_now_add=True)),
                ('message', models.CharField(blank=True, max_length=500, null=True)),
                ('payment_visited', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Intruder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=256)),
                ('reference', models.CharField(max_length=256)),
                ('transaction_date', models.DateTimeField(auto_now_add=True)),
                ('message', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MTNBundleTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=256)),
                ('email', models.EmailField(blank=True, max_length=250)),
                ('bundle_number', models.PositiveBigIntegerField()),
                ('offer', models.CharField(max_length=250)),
                ('reference', models.CharField(blank=True, max_length=20)),
                ('transaction_date', models.DateTimeField(auto_now_add=True)),
                ('transaction_status', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='OtherMTNBundleTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=256)),
                ('email', models.EmailField(blank=True, max_length=250)),
                ('bundle_number', models.PositiveBigIntegerField()),
                ('offer', models.CharField(max_length=250)),
                ('reference', models.CharField(blank=True, max_length=20)),
                ('transaction_date', models.DateTimeField(auto_now_add=True)),
                ('transaction_status', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SikaKokooBundleTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=256)),
                ('email', models.EmailField(blank=True, max_length=250)),
                ('bundle_number', models.PositiveBigIntegerField()),
                ('offer', models.CharField(max_length=250)),
                ('reference', models.CharField(blank=True, max_length=20)),
                ('transaction_date', models.DateTimeField(auto_now_add=True)),
                ('transaction_status', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='TvTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=256)),
                ('email', models.EmailField(blank=True, max_length=250)),
                ('account_number', models.PositiveIntegerField()),
                ('amount', models.PositiveIntegerField()),
                ('provider', models.CharField(max_length=250)),
                ('reference', models.CharField(blank=True, max_length=20)),
                ('transaction_date', models.DateTimeField(auto_now_add=True)),
                ('transaction_status', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='VodafoneBundleTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=256)),
                ('email', models.EmailField(blank=True, max_length=250)),
                ('bundle_number', models.PositiveBigIntegerField()),
                ('offer', models.CharField(max_length=250)),
                ('reference', models.CharField(blank=True, max_length=20)),
                ('transaction_date', models.DateTimeField(auto_now_add=True)),
                ('transaction_status', models.CharField(max_length=100)),
            ],
        ),
    ]
