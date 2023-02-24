from django.shortcuts import render, redirect, reverse
import requests

from .. import models
from ..forms import BundleForm
from django.contrib import messages
import json
from django.http import HttpResponse
import random
from decouple import config


def pay_for_sk3_bundle(request):
    client_ref = 'gds'+str(random.randint(11111111, 99999999))

    if request.method == "POST":
        form = BundleForm(request.POST)
        if form.is_valid():
            phone_number = str(form.cleaned_data["phone"])
            amount = 2.90 

            url = "https://payproxyapi.hubtel.com/items/initiate"

            payload = json.dumps({
            "totalAmount": amount,
            "description": "Sika Kokoo 500MB (GHS 3 - 1 Day(s))",
            "callbackUrl": 'https://webhook.site/d53f5c53-eaba-4139-ad27-fb05b0a7be7f',
            "returnUrl": f'https://bestpay-app-id6nm.ondigitalocean.app/send_sk3_tigo_bundle/{client_ref}/{phone_number}',
            "cancellationUrl": "https://www.google.com",
            "merchantAccountNumber": "2017101",
            "clientReference": client_ref
            })
            headers = {
            'Authorization': config("HUBTEL_API_KEY"),
            'Content-Type': 'application/json'
            }

            response = requests.request("POST", url, headers=headers, data=payload)
            print(response.json())
            data = response.json()
            print(data)

            if data["status"] == "Success":
                checkout = data['data']['checkoutUrl']
                return redirect(checkout)
            else:
                messages.info(request, "Failed. Try again later")
            return render(request, 'store/layouts/tigo_bundle.html', context={'form': form})
    else:
        form = BundleForm(initial={'phone':233})
    return render(request, "store/layouts/tigo_bundle.html", {'form': form})


def send_sk3_bundle(request, client_ref, phone_number, username, email):
    global ref_needed
    global status_needed
    global content_needed
    payment = models.AppPayment.objects.filter(reference=client_ref, payment_visited=True)
    if payment:
        new_intruder = models.Intruder.objects.create(
            username=username,
            reference=client_ref,
            message="Payment already exists and the reference has expired. User tried using it again."
        )
        new_intruder.save()
        return redirect('intruder')
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        "api-key": "8f56b7ea-e1d0-4ce7-ace0-162f7dc55a39"
    }
    webhook_response = requests.request("GET",
                                        "https://webhook.site/token/d53f5c53-eaba-4139-ad27-fb05b0a7be7f/requests?sorting=newest",
                                        headers=headers)

    json_webhook_response = webhook_response.json()['data']
    txns_list = []
    ref_list = []
    for txn in json_webhook_response:
        txns_list.append(txn)
    for item in txns_list:
        content = json.loads(item["content"])
        ref = content["Data"]["ClientReference"]
        status = content["Status"]
        print(ref)
        print(status)
        if ref == client_ref:
            print("========================================================")
            print("========================================================")
            print("=======================Ref=================================")
            print(ref)
            print("=====================Client Ref================================")
            print(client_ref)
            ref_needed = ref
            status_needed = status
            content_needed = content
            break

    if ref_needed == client_ref and status_needed == "Success":
        momo_number = content_needed["Data"]["CustomerPhoneNumber"]
        webhook_amount = content_needed["Data"]["Amount"]
        payment_description = content_needed["Data"]["Description"]
        print(f"{status_needed}--{ref_needed}--{momo_number}--{webhook_amount}--{payment_description}")
        payment = models.AppPayment.objects.filter(username=username, reference=client_ref, payment_visited=True)

        if payment:
            new_intruder = models.Intruder.objects.create(
                username=username,
                reference=client_ref,
                message="Payment already exists and the reference has expired. User tried using it again."
            )
            new_intruder.save()
            return redirect("intruder")
        else:
            new_payment = models.AppPayment.objects.create(
                username=username,
                reference=client_ref,
                payment_number=momo_number,
                amount=webhook_amount,
                payment_description=payment_description,
                transaction_status=status_needed,
                payment_visited=True,
                message="Payment verified successfully",
            )
            new_payment.save()

            reference = f"\"{client_ref}\""
            url = "https://cs.hubtel.com/commissionservices/2016884/06abd92da459428496967612463575ca"

            payload = "{\r\n    \"Destination\": " + phone_number + ",\r\n    \"Amount\": 3.0,\r\n    \"CallbackUrl\": \"https://webhook.site/9125cb31-9481-47ad-972f-d1d7765a5957\",\r\n    \"ClientReference\": " + reference + ",\r\n    \"Extradata\" : {\r\n        \"bundle\" : \"SK3\"\r\n    }\r\n}\r\n"
            headers = {
                'Authorization': config("HUBTEL_API_KEY"),
                'Content-Type': 'text/plain'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            if response.status_code == 200:
                new_airtime_transaction = models.SikaKokooBundleTransaction.objects.create(
                    username=username,
                    email=email,
                    bundle_number=phone_number,
                    offer="SK3",
                    reference=client_ref,
                    transaction_status="Success"
                )
                new_airtime_transaction.save()
                return redirect('thank_you')
            else:
                print("not 200 error")
                new_airtime_transaction = models.SikaKokooBundleTransaction.objects.create(
                    username=username,
                    email=email,
                    bundle_number=phone_number,
                    offer="SK3",
                    reference=client_ref,
                    transaction_status="Failed"
                )
                new_airtime_transaction.save()
                return redirect("failed")
    else:
        new_airtime_transaction = models.SikaKokooBundleTransaction.objects.create(
            username=username,
            email=email,
            bundle_number=phone_number,
            offer="SK3",
            reference=client_ref,
            transaction_status="Failed"
        )
        new_airtime_transaction.save()
        print("last error")
        return redirect("failed")

######################################### 5 Cedis sk ######################################################

def pay_for_sk5_bundle(request):
    client_ref = 'gds'+str(random.randint(11111111, 99999999))

    if request.method == "POST":
        form = BundleForm(request.POST)
        if form.is_valid():
            phone_number = str(form.cleaned_data["phone"])
            amount = 4.90 

            url = "https://payproxyapi.hubtel.com/items/initiate"

            payload = json.dumps({
            "totalAmount": amount,
            "description": "Sika Kokoo 900MB (GHS 5 - 3 Day(s))",
            "callbackUrl": 'https://webhook.site/d53f5c53-eaba-4139-ad27-fb05b0a7be7f',
            "returnUrl": f'https://bestpay-app-id6nm.ondigitalocean.app/send_sk5_tigo_bundle/{client_ref}/{phone_number}',
            "cancellationUrl": "https://www.google.com",
            "merchantAccountNumber": "2017101",
            "clientReference": client_ref
            })
            headers = {
            'Authorization': config("HUBTEL_API_KEY"),
            'Content-Type': 'application/json'
            }

            response = requests.request("POST", url, headers=headers, data=payload)
            print(response.json())
            data = response.json()
            print(data)

            if data["status"] == "Success":
                checkout = data['data']['checkoutUrl']
                return redirect(checkout)
            else:
                messages.info(request, "Failed. Try again later")
            return render(request, 'store/layouts/tigo_bundle.html', context={'form': form})
    else:
        form = BundleForm(initial={'phone':233})
    return render(request, "store/layouts/tigo_bundle.html", {'form': form})


def send_sk5_bundle(request, client_ref, phone_number, username, email):
    global ref_needed
    global status_needed
    global content_needed
    payment = models.AppPayment.objects.filter(reference=client_ref, payment_visited=True)
    if payment:
        new_intruder = models.Intruder.objects.create(
            username=username,
            reference=client_ref,
            message="Payment already exists and the reference has expired. User tried using it again."
        )
        new_intruder.save()
        return redirect('intruder')
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        "api-key": "8f56b7ea-e1d0-4ce7-ace0-162f7dc55a39"
    }
    webhook_response = requests.request("GET",
                                        "https://webhook.site/token/d53f5c53-eaba-4139-ad27-fb05b0a7be7f/requests?sorting=newest",
                                        headers=headers)

    json_webhook_response = webhook_response.json()['data']
    txns_list = []
    ref_list = []
    for txn in json_webhook_response:
        txns_list.append(txn)
    for item in txns_list:
        content = json.loads(item["content"])
        ref = content["Data"]["ClientReference"]
        status = content["Status"]
        print(ref)
        print(status)
        if ref == client_ref:
            print("========================================================")
            print("========================================================")
            print("=======================Ref=================================")
            print(ref)
            print("=====================Client Ref================================")
            print(client_ref)
            ref_needed = ref
            status_needed = status
            content_needed = content
            break

    if ref_needed == client_ref and status_needed == "Success":
        momo_number = content_needed["Data"]["CustomerPhoneNumber"]
        webhook_amount = content_needed["Data"]["Amount"]
        payment_description = content_needed["Data"]["Description"]
        print(f"{status_needed}--{ref_needed}--{momo_number}--{webhook_amount}--{payment_description}")
        payment = models.AppPayment.objects.filter(username=username, reference=client_ref, payment_visited=True)

        if payment:
            new_intruder = models.Intruder.objects.create(
                username=username,
                reference=client_ref,
                message="Payment already exists and the reference has expired. User tried using it again."
            )
            new_intruder.save()
            return redirect("intruder")
        else:
            new_payment = models.AppPayment.objects.create(
                username=username,
                reference=client_ref,
                payment_number=momo_number,
                amount=webhook_amount,
                payment_description=payment_description,
                transaction_status=status_needed,
                payment_visited=True,
                message="Payment verified successfully",
            )
            new_payment.save()

            reference = f"\"{client_ref}\""
            url = "https://cs.hubtel.com/commissionservices/2016884/06abd92da459428496967612463575ca"

            payload = "{\r\n    \"Destination\": " + phone_number + ",\r\n    \"Amount\": 5.0,\r\n    \"CallbackUrl\": \"https://webhook.site/9125cb31-9481-47ad-972f-d1d7765a5957\",\r\n    \"ClientReference\": " + reference + ",\r\n    \"Extradata\" : {\r\n        \"bundle\" : \"SK5\"\r\n    }\r\n}\r\n"
            headers = {
                'Authorization': config("HUBTEL_API_KEY"),
                'Content-Type': 'text/plain'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            if response.status_code == 200:
                new_airtime_transaction = models.SikaKokooBundleTransaction.objects.create(
                    username=username,
                    email=email,
                    bundle_number=phone_number,
                    offer="SK5",
                    reference=client_ref,
                    transaction_status="Success"
                )
                new_airtime_transaction.save()
                return redirect('thank_you')
            else:
                print("not 200 error")
                new_airtime_transaction = models.SikaKokooBundleTransaction.objects.create(
                    username=username,
                    email=email,
                    bundle_number=phone_number,
                    offer="SK5",
                    reference=client_ref,
                    transaction_status="Failed"
                )
                new_airtime_transaction.save()
                return redirect("failed")
    else:
        new_airtime_transaction = models.SikaKokooBundleTransaction.objects.create(
            username=username,
            email=email,
            bundle_number=phone_number,
            offer="SK5",
            reference=client_ref,
            transaction_status="Failed"
        )
        new_airtime_transaction.save()
        print("last error")
        return redirect("failed")

######################################### 6 Cedis sk ######################################################

def pay_for_sk6_bundle(request):
    client_ref = 'gds'+str(random.randint(11111111, 99999999))

    if request.method == "POST":
        form = BundleForm(request.POST)
        if form.is_valid():
            phone_number = str(form.cleaned_data["phone"])
            amount = 5.90

            url = "https://payproxyapi.hubtel.com/items/initiate"

            payload = json.dumps({
            "totalAmount": amount,
            "description": "Sika Kokoo 1.2GB (GHS 6 - 2 Day(s))",
            "callbackUrl": 'https://webhook.site/d53f5c53-eaba-4139-ad27-fb05b0a7be7f',
            "returnUrl": f'https://bestpay-app-id6nm.ondigitalocean.app/send_sk6_tigo_bundle/{client_ref}/{phone_number}',
            "cancellationUrl": "https://www.google.com",
            "merchantAccountNumber": "2017101",
            "clientReference": client_ref
            })
            headers = {
            'Authorization': config("HUBTEL_API_KEY"),
            'Content-Type': 'application/json'
            }

            response = requests.request("POST", url, headers=headers, data=payload)
            print(response.json())
            data = response.json()
            print(data)

            if data["status"] == "Success":
                checkout = data['data']['checkoutUrl']
                return redirect(checkout)
            else:
                messages.info(request, "Failed. Try again later")
            return render(request, 'store/layouts/tigo_bundle.html', context={'form': form})
    else:
        form = BundleForm(initial={'phone':233})
    return render(request, "store/layouts/tigo_bundle.html", {'form': form})


def send_sk6_bundle(request, client_ref, phone_number, username, email):
    global ref_needed
    global status_needed
    global content_needed
    payment = models.AppPayment.objects.filter(reference=client_ref, payment_visited=True)
    if payment:
        new_intruder = models.Intruder.objects.create(
            username=username,
            reference=client_ref,
            message="Payment already exists and the reference has expired. User tried using it again."
        )
        new_intruder.save()
        return redirect('intruder')
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        "api-key": "8f56b7ea-e1d0-4ce7-ace0-162f7dc55a39"
    }
    webhook_response = requests.request("GET",
                                        "https://webhook.site/token/d53f5c53-eaba-4139-ad27-fb05b0a7be7f/requests?sorting=newest",
                                        headers=headers)

    json_webhook_response = webhook_response.json()['data']
    txns_list = []
    ref_list = []
    for txn in json_webhook_response:
        txns_list.append(txn)
    for item in txns_list:
        content = json.loads(item["content"])
        ref = content["Data"]["ClientReference"]
        status = content["Status"]
        print(ref)
        print(status)
        if ref == client_ref:
            print("========================================================")
            print("========================================================")
            print("=======================Ref=================================")
            print(ref)
            print("=====================Client Ref================================")
            print(client_ref)
            ref_needed = ref
            status_needed = status
            content_needed = content
            break

    if ref_needed == client_ref and status_needed == "Success":
        momo_number = content_needed["Data"]["CustomerPhoneNumber"]
        webhook_amount = content_needed["Data"]["Amount"]
        payment_description = content_needed["Data"]["Description"]
        print(f"{status_needed}--{ref_needed}--{momo_number}--{webhook_amount}--{payment_description}")
        payment = models.AppPayment.objects.filter(username=username, reference=client_ref, payment_visited=True)

        if payment:
            new_intruder = models.Intruder.objects.create(
                username=username,
                reference=client_ref,
                message="Payment already exists and the reference has expired. User tried using it again."
            )
            new_intruder.save()
            return redirect("intruder")
        else:
            new_payment = models.AppPayment.objects.create(
                username=username,
                reference=client_ref,
                payment_number=momo_number,
                amount=webhook_amount,
                payment_description=payment_description,
                transaction_status=status_needed,
                payment_visited=True,
                message="Payment verified successfully",
            )
            new_payment.save()

            reference = f"\"{client_ref}\""
            url = "https://cs.hubtel.com/commissionservices/2016884/06abd92da459428496967612463575ca"

            payload = "{\r\n    \"Destination\": " + phone_number + ",\r\n    \"Amount\": 6.0,\r\n    \"CallbackUrl\": \"https://webhook.site/9125cb31-9481-47ad-972f-d1d7765a5957\",\r\n    \"ClientReference\": " + reference + ",\r\n    \"Extradata\" : {\r\n        \"bundle\" : \"SK6\"\r\n    }\r\n}\r\n"
            headers = {
                'Authorization': config("HUBTEL_API_KEY"),
                'Content-Type': 'text/plain'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            if response.status_code == 200:
                new_airtime_transaction = models.SikaKokooBundleTransaction.objects.create(
                    username=username,
                    email=email,
                    bundle_number=phone_number,
                    offer="SK6",
                    reference=client_ref,
                    transaction_status="Success"
                )
                new_airtime_transaction.save()
                return redirect('thank_you')
            else:
                print("not 200 error")
                new_airtime_transaction = models.SikaKokooBundleTransaction.objects.create(
                    username=username,
                    email=email,
                    bundle_number=phone_number,
                    offer="SK6",
                    reference=client_ref,
                    transaction_status="Failed"
                )
                new_airtime_transaction.save()
                return redirect("failed")
    else:
        new_airtime_transaction = models.SikaKokooBundleTransaction.objects.create(
            username=username,
            email=email,
            bundle_number=phone_number,
            offer="SK6",
            reference=client_ref,
            transaction_status="Failed"
        )
        new_airtime_transaction.save()
        print("last error")
        return redirect("failed")
######################################### 10 Cedis sk ######################################################

def pay_for_sk10_bundle(request):
    client_ref = 'gds'+str(random.randint(11111111, 99999999))

    if request.method == "POST":
        form = BundleForm(request.POST)
        if form.is_valid():
            phone_number = str(form.cleaned_data["phone"])
            amount = 9.90

            url = "https://payproxyapi.hubtel.com/items/initiate"

            payload = json.dumps({
            "totalAmount": amount,
            "description": "Sika Kokoo 1.4GB (GHS 10 - 5 Day(s))",
            "callbackUrl": 'https://webhook.site/d53f5c53-eaba-4139-ad27-fb05b0a7be7f',
            "returnUrl": f'https://bestpay-app-id6nm.ondigitalocean.app/send_sk10_tigo_bundle/{client_ref}/{phone_number}',
            "cancellationUrl": "https://www.google.com",
            "merchantAccountNumber": "2017101",
            "clientReference": client_ref
            })
            headers = {
            'Authorization': config("HUBTEL_API_KEY"),
            'Content-Type': 'application/json'
            }

            response = requests.request("POST", url, headers=headers, data=payload)
            print(response.json())
            data = response.json()
            print(data)

            if data["status"] == "Success":
                checkout = data['data']['checkoutUrl']
                return redirect(checkout)
            else:
                messages.info(request, "Failed. Try again later")
            return render(request, 'store/layouts/tigo_bundle.html', context={'form': form})
    else:
        form = BundleForm(initial={'phone':233})
    return render(request, "store/layouts/tigo_bundle.html", {'form': form})


def send_sk10_bundle(request, client_ref, phone_number, username, email):
    global ref_needed
    global status_needed
    global content_needed
    payment = models.AppPayment.objects.filter(reference=client_ref, payment_visited=True)
    if payment:
        new_intruder = models.Intruder.objects.create(
            username=username,
            reference=client_ref,
            message="Payment already exists and the reference has expired. User tried using it again."
        )
        new_intruder.save()
        return redirect('intruder')
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        "api-key": "8f56b7ea-e1d0-4ce7-ace0-162f7dc55a39"
    }
    webhook_response = requests.request("GET",
                                        "https://webhook.site/token/d53f5c53-eaba-4139-ad27-fb05b0a7be7f/requests?sorting=newest",
                                        headers=headers)

    json_webhook_response = webhook_response.json()['data']
    txns_list = []
    ref_list = []
    for txn in json_webhook_response:
        txns_list.append(txn)
    for item in txns_list:
        content = json.loads(item["content"])
        ref = content["Data"]["ClientReference"]
        status = content["Status"]
        print(ref)
        print(status)
        if ref == client_ref:
            print("========================================================")
            print("========================================================")
            print("=======================Ref=================================")
            print(ref)
            print("=====================Client Ref================================")
            print(client_ref)
            ref_needed = ref
            status_needed = status
            content_needed = content
            break

    if ref_needed == client_ref and status_needed == "Success":
        momo_number = content_needed["Data"]["CustomerPhoneNumber"]
        webhook_amount = content_needed["Data"]["Amount"]
        payment_description = content_needed["Data"]["Description"]
        print(f"{status_needed}--{ref_needed}--{momo_number}--{webhook_amount}--{payment_description}")
        payment = models.AppPayment.objects.filter(username=username, reference=client_ref, payment_visited=True)

        if payment:
            new_intruder = models.Intruder.objects.create(
                username=username,
                reference=client_ref,
                message="Payment already exists and the reference has expired. User tried using it again."
            )
            new_intruder.save()
            return redirect("intruder")
        else:
            new_payment = models.AppPayment.objects.create(
                username=username,
                reference=client_ref,
                payment_number=momo_number,
                amount=webhook_amount,
                payment_description=payment_description,
                transaction_status=status_needed,
                payment_visited=True,
                message="Payment verified successfully",
            )
            new_payment.save()

            reference = f"\"{client_ref}\""
            url = "https://cs.hubtel.com/commissionservices/2016884/06abd92da459428496967612463575ca"

            payload = "{\r\n    \"Destination\": " + phone_number + ",\r\n    \"Amount\": 10.0,\r\n    \"CallbackUrl\": \"https://webhook.site/9125cb31-9481-47ad-972f-d1d7765a5957\",\r\n    \"ClientReference\": " + reference + ",\r\n    \"Extradata\" : {\r\n        \"bundle\" : \"SK10\"\r\n    }\r\n}\r\n"
            headers = {
                'Authorization': config("HUBTEL_API_KEY"),
                'Content-Type': 'text/plain'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            if response.status_code == 200:
                new_airtime_transaction = models.SikaKokooBundleTransaction.objects.create(
                    username=username,
                    email=email,
                    bundle_number=phone_number,
                    offer="SK10",
                    reference=client_ref,
                    transaction_status="Success"
                )
                new_airtime_transaction.save()
                return redirect('thank_you')
            else:
                print("not 200 error")
                new_airtime_transaction = models.SikaKokooBundleTransaction.objects.create(
                    username=username,
                    email=email,
                    bundle_number=phone_number,
                    offer="SK10",
                    reference=client_ref,
                    transaction_status="Failed"
                )
                new_airtime_transaction.save()
                return redirect("failed")
    else:
        new_airtime_transaction = models.SikaKokooBundleTransaction.objects.create(
            username=username,
            email=email,
            bundle_number=phone_number,
            offer="SK10",
            reference=client_ref,
            transaction_status="Failed"
        )
        new_airtime_transaction.save()
        print("last error")
        return redirect("failed")

######################################### 11 Cedis sk ######################################################

def pay_for_sk11_bundle(request):
    client_ref = 'gds'+str(random.randint(11111111, 99999999))

    if request.method == "POST":
        form = BundleForm(request.POST)
        if form.is_valid():
            phone_number = str(form.cleaned_data["phone"])
            amount = 10.50

            url = "https://payproxyapi.hubtel.com/items/initiate"

            payload = json.dumps({
            "totalAmount": amount,
            "description": "Sika Kokoo 2GB (GHS 11 - 2 Day(s))",
            "callbackUrl": 'https://webhook.site/d53f5c53-eaba-4139-ad27-fb05b0a7be7f',
            "returnUrl": f'https://bestpay-app-id6nm.ondigitalocean.app/send_sk11_tigo_bundle/{client_ref}/{phone_number}',
            "cancellationUrl": "https://www.google.com",
            "merchantAccountNumber": "2017101",
            "clientReference": client_ref
            })
            headers = {
            'Authorization': config("HUBTEL_API_KEY"),
            'Content-Type': 'application/json'
            }

            response = requests.request("POST", url, headers=headers, data=payload)
            print(response.json())
            data = response.json()
            print(data)

            if data["status"] == "Success":
                checkout = data['data']['checkoutUrl']
                return redirect(checkout)
            else:
                messages.info(request, "Failed. Try again later")
            return render(request, 'store/layouts/tigo_bundle.html', context={'form': form})
    else:
        form = BundleForm(initial={'phone':233})
    return render(request, "store/layouts/tigo_bundle.html", {'form': form})


def send_sk11_bundle(request, client_ref, phone_number, username, email):
    global ref_needed
    global status_needed
    global content_needed
    payment = models.AppPayment.objects.filter(reference=client_ref, payment_visited=True)
    if payment:
        new_intruder = models.Intruder.objects.create(
            username=username,
            reference=client_ref,
            message="Payment already exists and the reference has expired. User tried using it again."
        )
        new_intruder.save()
        return redirect('intruder')
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        "api-key": "8f56b7ea-e1d0-4ce7-ace0-162f7dc55a39"
    }
    webhook_response = requests.request("GET",
                                        "https://webhook.site/token/d53f5c53-eaba-4139-ad27-fb05b0a7be7f/requests?sorting=newest",
                                        headers=headers)

    json_webhook_response = webhook_response.json()['data']
    txns_list = []
    ref_list = []
    for txn in json_webhook_response:
        txns_list.append(txn)
    for item in txns_list:
        content = json.loads(item["content"])
        ref = content["Data"]["ClientReference"]
        status = content["Status"]
        print(ref)
        print(status)
        if ref == client_ref:
            print("========================================================")
            print("========================================================")
            print("=======================Ref=================================")
            print(ref)
            print("=====================Client Ref================================")
            print(client_ref)
            ref_needed = ref
            status_needed = status
            content_needed = content
            break

    if ref_needed == client_ref and status_needed == "Success":
        momo_number = content_needed["Data"]["CustomerPhoneNumber"]
        webhook_amount = content_needed["Data"]["Amount"]
        payment_description = content_needed["Data"]["Description"]
        print(f"{status_needed}--{ref_needed}--{momo_number}--{webhook_amount}--{payment_description}")
        payment = models.AppPayment.objects.filter(username=username, reference=client_ref, payment_visited=True)

        if payment:
            new_intruder = models.Intruder.objects.create(
                username=username,
                reference=client_ref,
                message="Payment already exists and the reference has expired. User tried using it again."
            )
            new_intruder.save()
            return redirect("intruder")
        else:
            new_payment = models.AppPayment.objects.create(
                username=username,
                reference=client_ref,
                payment_number=momo_number,
                amount=webhook_amount,
                payment_description=payment_description,
                transaction_status=status_needed,
                payment_visited=True,
                message="Payment verified successfully",
            )
            new_payment.save()

            reference = f"\"{client_ref}\""
            url = "https://cs.hubtel.com/commissionservices/2016884/06abd92da459428496967612463575ca"

            payload = "{\r\n    \"Destination\": " + phone_number + ",\r\n    \"Amount\": 11.0,\r\n    \"CallbackUrl\": \"https://webhook.site/9125cb31-9481-47ad-972f-d1d7765a5957\",\r\n    \"ClientReference\": " + reference + ",\r\n    \"Extradata\" : {\r\n        \"bundle\" : \"SK11\"\r\n    }\r\n}\r\n"
            headers = {
                'Authorization': config("HUBTEL_API_KEY"),
                'Content-Type': 'text/plain'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            if response.status_code == 200:
                new_airtime_transaction = models.SikaKokooBundleTransaction.objects.create(
                    username=username,
                    email=email,
                    bundle_number=phone_number,
                    offer="SK11",
                    reference=client_ref,
                    transaction_status="Success"
                )
                new_airtime_transaction.save()
                return redirect('thank_you')
            else:
                print("not 200 error")
                new_airtime_transaction = models.SikaKokooBundleTransaction.objects.create(
                    username=username,
                    email=email,
                    bundle_number=phone_number,
                    offer="SK11",
                    reference=client_ref,
                    transaction_status="Failed"
                )
                new_airtime_transaction.save()
                return redirect("failed")
    else:
        new_airtime_transaction = models.SikaKokooBundleTransaction.objects.create(
            username=username,
            email=email,
            bundle_number=phone_number,
            offer="SK11",
            reference=client_ref,
            transaction_status="Failed"
        )
        new_airtime_transaction.save()
        print("last error")
        return redirect("failed")

######################################### 15 Cedis sk ######################################################

def pay_for_sk15_bundle(request):
    client_ref = 'gds'+str(random.randint(11111111, 99999999))

    if request.method == "POST":
        form = BundleForm(request.POST)
        if form.is_valid():
            phone_number = str(form.cleaned_data["phone"])
            amount = 14.50

            url = "https://payproxyapi.hubtel.com/items/initiate"

            payload = json.dumps({
            "totalAmount": amount,
            "description": "Sika Kokoo 2.6GB (GHS 15 - 4 Day(s))",
            "callbackUrl": 'https://webhook.site/d53f5c53-eaba-4139-ad27-fb05b0a7be7f',
            "returnUrl": f'https://bestpay-app-id6nm.ondigitalocean.app/send_sk15_tigo_bundle/{client_ref}/{phone_number}',
            "cancellationUrl": "https://www.google.com",
            "merchantAccountNumber": "2017101",
            "clientReference": client_ref
            })
            headers = {
            'Authorization': config("HUBTEL_API_KEY"),
            'Content-Type': 'application/json'
            }

            response = requests.request("POST", url, headers=headers, data=payload)
            print(response.json())
            data = response.json()
            print(data)

            if data["status"] == "Success":
                checkout = data['data']['checkoutUrl']
                return redirect(checkout)
            else:
                messages.info(request, "Failed. Try again later")
            return render(request, 'store/layouts/tigo_bundle.html', context={'form': form})
    else:
        form = BundleForm(initial={'phone':233})
    return render(request, "store/layouts/tigo_bundle.html", {'form': form})


def send_sk15_bundle(request, client_ref, phone_number, username, email):
    global ref_needed
    global status_needed
    global content_needed
    payment = models.AppPayment.objects.filter(reference=client_ref, payment_visited=True)
    if payment:
        new_intruder = models.Intruder.objects.create(
            username=username,
            reference=client_ref,
            message="Payment already exists and the reference has expired. User tried using it again."
        )
        new_intruder.save()
        return redirect('intruder')
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        "api-key": "8f56b7ea-e1d0-4ce7-ace0-162f7dc55a39"
    }
    webhook_response = requests.request("GET",
                                        "https://webhook.site/token/d53f5c53-eaba-4139-ad27-fb05b0a7be7f/requests?sorting=newest",
                                        headers=headers)

    json_webhook_response = webhook_response.json()['data']
    txns_list = []
    ref_list = []
    for txn in json_webhook_response:
        txns_list.append(txn)
    for item in txns_list:
        content = json.loads(item["content"])
        ref = content["Data"]["ClientReference"]
        status = content["Status"]
        print(ref)
        print(status)
        if ref == client_ref:
            print("========================================================")
            print("========================================================")
            print("=======================Ref=================================")
            print(ref)
            print("=====================Client Ref================================")
            print(client_ref)
            ref_needed = ref
            status_needed = status
            content_needed = content
            break

    if ref_needed == client_ref and status_needed == "Success":
        momo_number = content_needed["Data"]["CustomerPhoneNumber"]
        webhook_amount = content_needed["Data"]["Amount"]
        payment_description = content_needed["Data"]["Description"]
        print(f"{status_needed}--{ref_needed}--{momo_number}--{webhook_amount}--{payment_description}")
        payment = models.AppPayment.objects.filter(username=username, reference=client_ref, payment_visited=True)

        if payment:
            new_intruder = models.Intruder.objects.create(
                username=username,
                reference=client_ref,
                message="Payment already exists and the reference has expired. User tried using it again."
            )
            new_intruder.save()
            return redirect("intruder")
        else:
            new_payment = models.AppPayment.objects.create(
                username=username,
                reference=client_ref,
                payment_number=momo_number,
                amount=webhook_amount,
                payment_description=payment_description,
                transaction_status=status_needed,
                payment_visited=True,
                message="Payment verified successfully",
            )
            new_payment.save()

            reference = f"\"{client_ref}\""
            url = "https://cs.hubtel.com/commissionservices/2016884/06abd92da459428496967612463575ca"

            payload = "{\r\n    \"Destination\": " + phone_number + ",\r\n    \"Amount\": 15.0,\r\n    \"CallbackUrl\": \"https://webhook.site/9125cb31-9481-47ad-972f-d1d7765a5957\",\r\n    \"ClientReference\": " + reference + ",\r\n    \"Extradata\" : {\r\n        \"bundle\" : \"SK15\"\r\n    }\r\n}\r\n"
            headers = {
                'Authorization': config("HUBTEL_API_KEY"),
                'Content-Type': 'text/plain'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            if response.status_code == 200:
                new_airtime_transaction = models.SikaKokooBundleTransaction.objects.create(
                    username=username,
                    email=email,
                    bundle_number=phone_number,
                    offer="SK15",
                    reference=client_ref,
                    transaction_status="Success"
                )
                new_airtime_transaction.save()
                return redirect('thank_you')
            else:
                print("not 200 error")
                new_airtime_transaction = models.SikaKokooBundleTransaction.objects.create(
                    username=username,
                    email=email,
                    bundle_number=phone_number,
                    offer="SK15",
                    reference=client_ref,
                    transaction_status="Failed"
                )
                new_airtime_transaction.save()
                return redirect("failed")
    else:
        new_airtime_transaction = models.SikaKokooBundleTransaction.objects.create(
            username=username,
            email=email,
            bundle_number=phone_number,
            offer="SK15",
            reference=client_ref,
            transaction_status="Failed"
        )
        new_airtime_transaction.save()
        print("last error")
        return redirect("failed")

######################################### 20 Cedis sk ######################################################

def pay_for_sk20_bundle(request):
    client_ref = 'gds'+str(random.randint(11111111, 99999999))

    if request.method == "POST":
        form = BundleForm(request.POST)
        if form.is_valid():
            phone_number = str(form.cleaned_data["phone"])
            amount = 19.50

            url = "https://payproxyapi.hubtel.com/items/initiate"

            payload = json.dumps({
            "totalAmount": amount,
            "description": "Sika Kokoo 3GB (GHS 20 - 5 Day(s))",
            "callbackUrl": 'https://webhook.site/d53f5c53-eaba-4139-ad27-fb05b0a7be7f',
            "returnUrl": f'https://bestpay-app-id6nm.ondigitalocean.app/send_sk20_tigo_bundle/{client_ref}/{phone_number}',
            "cancellationUrl": "https://www.google.com",
            "merchantAccountNumber": "2017101",
            "clientReference": client_ref
            })
            headers = {
            'Authorization': config("HUBTEL_API_KEY"),
            'Content-Type': 'application/json'
            }

            response = requests.request("POST", url, headers=headers, data=payload)
            print(response.json())
            data = response.json()
            print(data)

            if data["status"] == "Success":
                checkout = data['data']['checkoutUrl']
                return redirect(checkout)
            else:
                messages.info(request, "Failed. Try again later")
            return render(request, 'store/layouts/tigo_bundle.html', context={'form': form})
    else:
        form = BundleForm(initial={'phone':233})
    return render(request, "store/layouts/tigo_bundle.html", {'form': form})


def send_sk20_bundle(request, client_ref, phone_number, username, email):
    global ref_needed
    global status_needed
    global content_needed
    payment = models.AppPayment.objects.filter(reference=client_ref, payment_visited=True)
    if payment:
        new_intruder = models.Intruder.objects.create(
            username=username,
            reference=client_ref,
            message="Payment already exists and the reference has expired. User tried using it again."
        )
        new_intruder.save()
        return redirect('intruder')
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        "api-key": "8f56b7ea-e1d0-4ce7-ace0-162f7dc55a39"
    }
    webhook_response = requests.request("GET",
                                        "https://webhook.site/token/d53f5c53-eaba-4139-ad27-fb05b0a7be7f/requests?sorting=newest",
                                        headers=headers)

    json_webhook_response = webhook_response.json()['data']
    txns_list = []
    ref_list = []
    for txn in json_webhook_response:
        txns_list.append(txn)
    for item in txns_list:
        content = json.loads(item["content"])
        ref = content["Data"]["ClientReference"]
        status = content["Status"]
        print(ref)
        print(status)
        if ref == client_ref:
            print("========================================================")
            print("========================================================")
            print("=======================Ref=================================")
            print(ref)
            print("=====================Client Ref================================")
            print(client_ref)
            ref_needed = ref
            status_needed = status
            content_needed = content
            break

    if ref_needed == client_ref and status_needed == "Success":
        momo_number = content_needed["Data"]["CustomerPhoneNumber"]
        webhook_amount = content_needed["Data"]["Amount"]
        payment_description = content_needed["Data"]["Description"]
        print(f"{status_needed}--{ref_needed}--{momo_number}--{webhook_amount}--{payment_description}")
        payment = models.AppPayment.objects.filter(username=username, reference=client_ref, payment_visited=True)

        if payment:
            new_intruder = models.Intruder.objects.create(
                username=username,
                reference=client_ref,
                message="Payment already exists and the reference has expired. User tried using it again."
            )
            new_intruder.save()
            return redirect("intruder")
        else:
            new_payment = models.AppPayment.objects.create(
                username=username,
                reference=client_ref,
                payment_number=momo_number,
                amount=webhook_amount,
                payment_description=payment_description,
                transaction_status=status_needed,
                payment_visited=True,
                message="Payment verified successfully",
            )
            new_payment.save()

            reference = f"\"{client_ref}\""
            url = "https://cs.hubtel.com/commissionservices/2016884/06abd92da459428496967612463575ca"

            payload = "{\r\n    \"Destination\": " + phone_number + ",\r\n    \"Amount\": 20.0,\r\n    \"CallbackUrl\": \"https://webhook.site/9125cb31-9481-47ad-972f-d1d7765a5957\",\r\n    \"ClientReference\": " + reference + ",\r\n    \"Extradata\" : {\r\n        \"bundle\" : \"SK20\"\r\n    }\r\n}\r\n"
            headers = {
                'Authorization': config("HUBTEL_API_KEY"),
                'Content-Type': 'text/plain'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            if response.status_code == 200:
                new_airtime_transaction = models.SikaKokooBundleTransaction.objects.create(
                    username=username,
                    email=email,
                    bundle_number=phone_number,
                    offer="SK20",
                    reference=client_ref,
                    transaction_status="Success"
                )
                new_airtime_transaction.save()
                return redirect('thank_you')
            else:
                print("not 200 error")
                new_airtime_transaction = models.SikaKokooBundleTransaction.objects.create(
                    username=username,
                    email=email,
                    bundle_number=phone_number,
                    offer="SK20",
                    reference=client_ref,
                    transaction_status="Failed"
                )
                new_airtime_transaction.save()
                return redirect("failed")
    else:
        new_airtime_transaction = models.SikaKokooBundleTransaction.objects.create(
            username=username,
            email=email,
            bundle_number=phone_number,
            offer="SK20",
            reference=client_ref,
            transaction_status="Failed"
        )
        new_airtime_transaction.save()
        print("last error")
        return redirect("failed")
