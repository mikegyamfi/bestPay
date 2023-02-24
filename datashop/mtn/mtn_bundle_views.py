from django.shortcuts import render, redirect, reverse
import requests

from .. import models
from ..forms import BundleForm
from django.contrib import messages
import json
from django.http import HttpResponse
import random
from decouple import config

def pay_for_50p_bundle(request):
    client_ref = 'gds'+str(random.randint(11111111, 99999999))

    if request.method == "POST":
        form = BundleForm(request.POST)
        if form.is_valid():
            phone_number = str(form.cleaned_data["phone"])
            amount = 0.49    

            url = "https://payproxyapi.hubtel.com/items/initiate"

            payload = json.dumps({
            "totalAmount": amount,
            "description": "24.05MB Bundle",
            "callbackUrl": 'https://webhook.site/d53f5c53-eaba-4139-ad27-fb05b0a7be7f',
            "returnUrl": f'https://app.bestpaygh.com/send_0.5_mtn_bundle/{client_ref}/{phone_number}',
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
            return render(request, 'store/layouts/mtn_bundle.html', context={'form': form})
    else:
        form = BundleForm(initial={'phone':233})
    return render(request, "store/layouts/mtn_bundle.html", {'form': form})


def send_50p_bundle(request, client_ref, phone_number, username, email):
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
            url = "https://cs.hubtel.com/commissionservices/2016884/b230733cd56b4a0fad820e39f66bc27c"

            payload = "{\r\n    \"Destination\": " + phone_number + ",\r\n    \"Amount\": 0.5,\r\n    \"CallbackUrl\": \"https://webhook.site/9125cb31-9481-47ad-972f-d1d7765a5957\",\r\n    \"ClientReference\": " + reference + ",\r\n    \"Extradata\" : {\r\n        \"bundle\" : \"data_bundle_1\"\r\n    }\r\n}\r\n"
            headers = {
                'Authorization': config("HUBTEL_API_KEY"),
                'Content-Type': 'text/plain'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            if response.status_code == 200:
                new_mtn_transaction = models.MTNBundleTransaction.objects.create(
                    username=username,
                    email=email,
                    bundle_number=phone_number,
                    offer="50p Bundle",
                    reference=client_ref,
                    transaction_status="Success"
                )
                new_mtn_transaction.save()
                return redirect('thank_you')
            else:
                print("not 200 error")
                new_mtn_transaction = models.MTNBundleTransaction.objects.create(
                    username=username,
                    email=email,
                    bundle_number=phone_number,
                    offer="50p Bundle",
                    reference=client_ref,
                    transaction_status="Failed"
                )
                new_mtn_transaction.save()
                return redirect("failed")
    else:
        new_mtn_transaction = models.MTNBundleTransaction.objects.create(
            username=username,
            email=email,
            bundle_number=phone_number,
            offer="50p Bundle",
            reference=client_ref,
            transaction_status="Failed"
        )
        new_mtn_transaction.save()
        print("last error")
        return redirect("failed")

######################################### 1 CEDI BUNDLE ######################################################

def pay_for_1_bundle(request):
    client_ref = 'gds'+str(random.randint(11111111, 99999999))

    if request.method == "POST":
        form = BundleForm(request.POST)
        if form.is_valid():
            phone_number = str(form.cleaned_data["phone"])
            amount = 0.99  

            url = "https://payproxyapi.hubtel.com/items/initiate"

            payload = json.dumps({
            "totalAmount": amount,
            "description": "48.10MB Bundle",
            "callbackUrl": 'https://webhook.site/d53f5c53-eaba-4139-ad27-fb05b0a7be7f',
            "returnUrl": f'https://app.bestpaygh.com/send_1_mtn_bundle/{client_ref}/{phone_number}',
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
            return render(request, 'store/layouts/mtn_bundle.html', context={'form': form})
    else:
        form = BundleForm(initial={'phone':233})
    return render(request, "store/layouts/mtn_bundle.html", {'form': form})


def send_1_bundle(request, client_ref, phone_number, username, email):
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
            url = "https://cs.hubtel.com/commissionservices/2016884/b230733cd56b4a0fad820e39f66bc27c"

            payload = "{\r\n    \"Destination\": " + phone_number + ",\r\n    \"Amount\": 1,\r\n    \"CallbackUrl\": \"https://webhook.site/9125cb31-9481-47ad-972f-d1d7765a5957\",\r\n    \"ClientReference\": " + reference + ",\r\n    \"Extradata\" : {\r\n        \"bundle\" : \"data_bundle_2\"\r\n    }\r\n}\r\n"
            headers = {
                'Authorization': config("HUBTEL_API_KEY"),
                'Content-Type': 'text/plain'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            if response.status_code == 200:
                new_mtn_transaction = models.MTNBundleTransaction.objects.create(
                    username=username,
                    email=email,
                    bundle_number=phone_number,
                    offer="1 cedi Bundle",
                    reference=client_ref,
                    transaction_status="Success"
                )
                new_mtn_transaction.save()
                return redirect('thank_you')
            else:
                print("not 200 error")
                new_mtn_transaction = models.MTNBundleTransaction.objects.create(
                    username=username,
                    email=email,
                    bundle_number=phone_number,
                    offer="1 cedi Bundle",
                    reference=client_ref,
                    transaction_status="Failed"
                )
                new_mtn_transaction.save()
                return redirect("failed")
    else:
        new_mtn_transaction = models.MTNBundleTransaction.objects.create(
            username=username,
            email=email,
            bundle_number=phone_number,
            offer="1 cedi Bundle",
            reference=client_ref,
            transaction_status="Failed"
        )
        new_mtn_transaction.save()
        print("last error")
        return redirect("failed")

######################################### 2 CEDI BUNDLE ######################################################

######################################### 3 CEDI BUNDLE ######################################################

def pay_for_3_bundle(request):
    client_ref = 'gds'+str(random.randint(11111111, 99999999))

    if request.method == "POST":
        form = BundleForm(request.POST)
        if form.is_valid():
            phone_number = str(form.cleaned_data["phone"])
            amount = 2.90  

            url = "https://payproxyapi.hubtel.com/items/initiate"

            payload = json.dumps({
            "totalAmount": amount,
            "description": "471.70MB Bundle",
            "callbackUrl": 'https://webhook.site/d53f5c53-eaba-4139-ad27-fb05b0a7be7f',
            "returnUrl": f'https://app.bestpaygh.com/send_3_mtn_bundle/{client_ref}/{phone_number}',
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
            return render(request, 'store/layouts/mtn_bundle.html', context={'form': form})
    else:
        form = BundleForm(initial={'phone':233})
    return render(request, "store/layouts/mtn_bundle.html", {'form': form})


def send_3_bundle(request, client_ref, phone_number, username, email):
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
            url = "https://cs.hubtel.com/commissionservices/2016884/b230733cd56b4a0fad820e39f66bc27c"

            payload = "{\r\n    \"Destination\": " + phone_number + ",\r\n    \"Amount\": 3.0,\r\n    \"CallbackUrl\": \"https://webhook.site/9125cb31-9481-47ad-972f-d1d7765a5957\",\r\n    \"ClientReference\": " + reference + ",\r\n    \"Extradata\" : {\r\n        \"bundle\" : \"data_bundle_3\"\r\n    }\r\n}\r\n"
            headers = {
                'Authorization': config("HUBTEL_API_KEY"),
                'Content-Type': 'text/plain'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            if response.status_code == 200:
                new_mtn_transaction = models.MTNBundleTransaction.objects.create(
                    username=username,
                    email=email,
                    bundle_number=phone_number,
                    offer="3 cedis Bundle",
                    reference=client_ref,
                    transaction_status="Success"
                )
                new_mtn_transaction.save()
                return redirect('thank_you')
            else:
                print("not 200 error")
                new_mtn_transaction = models.MTNBundleTransaction.objects.create(
                    username=username,
                    email=email,
                    bundle_number=phone_number,
                    offer="3 cedis Bundle",
                    reference=client_ref,
                    transaction_status="Failed"
                )
                new_mtn_transaction.save()
                return redirect("failed")
    else:
        new_mtn_transaction = models.MTNBundleTransaction.objects.create(
            username=username,
            email=email,
            bundle_number=phone_number,
            offer="3 cedis Bundle",
            reference=client_ref,
            transaction_status="Failed"
        )
        new_mtn_transaction.save()
        print("last error")
        return redirect("failed")

######################################### 5 CEDI BUNDLE ######################################################

######################################### 10 CEDI BUNDLE ######################################################

def pay_for_10_bundle(request):
    client_ref = 'gds'+str(random.randint(11111111, 99999999))

    if request.method == "POST":
        form = BundleForm(request.POST)
        if form.is_valid():
            phone_number = str(form.cleaned_data["phone"])
            amount = 9.90

            url = "https://payproxyapi.hubtel.com/items/initiate"

            payload = json.dumps({
            "totalAmount": amount,
            "description": "971.82MB Bundle",
            "callbackUrl": 'https://webhook.site/d53f5c53-eaba-4139-ad27-fb05b0a7be7f',
            "returnUrl": f'https://app.bestpaygh.com/send_10_mtn_bundle/{client_ref}/{phone_number}',
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
            return render(request, 'store/layouts/mtn_bundle.html', context={'form': form})
    else:
        form = BundleForm(initial={'phone':233})
    return render(request, "store/layouts/mtn_bundle.html", {'form': form})


def send_10_bundle(request, client_ref, phone_number, username, email):
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
            url = "https://cs.hubtel.com/commissionservices/2016884/b230733cd56b4a0fad820e39f66bc27c"

            payload = "{\r\n    \"Destination\": " + phone_number + ",\r\n    \"Amount\": 10.0,\r\n    \"CallbackUrl\": \"https://webhook.site/9125cb31-9481-47ad-972f-d1d7765a5957\",\r\n    \"ClientReference\": " + reference + ",\r\n    \"Extradata\" : {\r\n        \"bundle\" : \"data_bundle_4\"\r\n    }\r\n}\r\n"
            headers = {
                'Authorization': config("HUBTEL_API_KEY"),
                'Content-Type': 'text/plain'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            if response.status_code == 200:
                new_mtn_transaction = models.MTNBundleTransaction.objects.create(
                    username=username,
                    email=email,
                    bundle_number=phone_number,
                    offer="10 cedis Bundle",
                    reference=client_ref,
                    transaction_status="Success"
                )
                new_mtn_transaction.save()
                return redirect('thank_you')
            else:
                print("not 200 error")
                new_mtn_transaction = models.MTNBundleTransaction.objects.create(
                    username=username,
                    email=email,
                    bundle_number=phone_number,
                    offer="10 cedis Bundle",
                    reference=client_ref,
                    transaction_status="Failed"
                )
                new_mtn_transaction.save()
                return redirect("failed")
    else:
        new_mtn_transaction = models.MTNBundleTransaction.objects.create(
            username=username,
            email=email,
            bundle_number=phone_number,
            offer="10 cedis Bundle",
            reference=client_ref,
            transaction_status="Failed"
        )
        new_mtn_transaction.save()
        print("last error")
        return redirect("failed")

######################################### 20 CEDI BUNDLE ######################################################

def pay_for_20_bundle(request):
    client_ref = 'gds'+str(random.randint(11111111, 99999999))

    if request.method == "POST":
        form = BundleForm(request.POST)
        if form.is_valid():
            phone_number = str(form.cleaned_data["phone"])
            amount = 19.50

            url = "https://payproxyapi.hubtel.com/items/initiate"

            payload = json.dumps({
            "totalAmount": amount,
            "description": "1.61GB Bundle",
            "callbackUrl": 'https://webhook.site/d53f5c53-eaba-4139-ad27-fb05b0a7be7f',
            "returnUrl": f'https://app.bestpaygh.com/send_20_mtn_bundle/{client_ref}/{phone_number}',
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
            return render(request, 'store/layouts/mtn_bundle.html', context={'form': form})
    else:
        form = BundleForm(initial={'phone':233})
    return render(request, "store/layouts/mtn_bundle.html", {'form': form})


def send_20_bundle(request, client_ref, phone_number, username, email):
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
            url = "https://cs.hubtel.com/commissionservices/2016884/b230733cd56b4a0fad820e39f66bc27c"

            payload = "{\r\n    \"Destination\": " + phone_number + ",\r\n    \"Amount\": 20.0,\r\n    \"CallbackUrl\": \"https://webhook.site/9125cb31-9481-47ad-972f-d1d7765a5957\",\r\n    \"ClientReference\": " + reference + ",\r\n    \"Extradata\" : {\r\n        \"bundle\" : \"flexi_data_bundle\"\r\n    }\r\n}\r\n"
            headers = {
                'Authorization': config("HUBTEL_API_KEY"),
                'Content-Type': 'text/plain'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            if response.status_code == 200:
                new_mtn_transaction = models.MTNBundleTransaction.objects.create(
                    username=username,
                    email=email,
                    bundle_number=phone_number,
                    offer="20 cedis Bundle",
                    reference=client_ref,
                    transaction_status="Success"
                )
                new_mtn_transaction.save()
                return redirect('thank_you')
            else:
                print("not 200 error")
                new_mtn_transaction = models.MTNBundleTransaction.objects.create(
                    username=username,
                    email=email,
                    bundle_number=phone_number,
                    offer="20 cedis Bundle",
                    reference=client_ref,
                    transaction_status="Failed"
                )
                new_mtn_transaction.save()
                return redirect("failed")
    else:
        new_mtn_transaction = models.MTNBundleTransaction.objects.create(
            username=username,
            email=email,
            bundle_number=phone_number,
            offer="20 cedis Bundle",
            reference=client_ref,
            transaction_status="Failed"
        )
        new_mtn_transaction.save()
        print("last error")
        return redirect("failed")

######################################### 40 CEDI BUNDLE ######################################################

def pay_for_40_bundle(request):
    client_ref = 'gds'+str(random.randint(11111111, 99999999))

    if request.method == "POST":
        form = BundleForm(request.POST)
        if form.is_valid():
            phone_number = str(form.cleaned_data["phone"])
            amount = 39.50

            url = "https://payproxyapi.hubtel.com/items/initiate"

            payload = json.dumps({
            "totalAmount": amount,
            "description": "3.23GB Bundle",
            "callbackUrl": 'https://webhook.site/d53f5c53-eaba-4139-ad27-fb05b0a7be7f',
            "returnUrl": f'https://app.bestpaygh.com/send_40_mtn_bundle/{client_ref}/{phone_number}',
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
            return render(request, 'store/layouts/mtn_bundle.html', context={'form': form})
    else:
        form = BundleForm(initial={'phone':233})
    return render(request, "store/layouts/mtn_bundle.html", {'form': form})


def send_40_bundle(request, client_ref, phone_number, username, email):
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
            url = "https://cs.hubtel.com/commissionservices/2016884/b230733cd56b4a0fad820e39f66bc27c"

            payload = "{\r\n    \"Destination\": " + phone_number + ",\r\n    \"Amount\": 40.0,\r\n    \"CallbackUrl\": \"https://webhook.site/9125cb31-9481-47ad-972f-d1d7765a5957\",\r\n    \"ClientReference\": " + reference + ",\r\n    \"Extradata\" : {\r\n        \"bundle\" : \"flexi_data_bundle\"\r\n    }\r\n}\r\n"
            headers = {
                'Authorization': config("HUBTEL_API_KEY"),
                'Content-Type': 'text/plain'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            if response.status_code == 200:
                new_mtn_transaction = models.MTNBundleTransaction.objects.create(
                    username=username,
                    email=email,
                    bundle_number=phone_number,
                    offer="40 cedis Bundle",
                    reference=client_ref,
                    transaction_status="Success"
                )
                new_mtn_transaction.save()
                return redirect('thank_you')
            else:
                print("not 200 error")
                new_mtn_transaction = models.MTNBundleTransaction.objects.create(
                    username=username,
                    email=email,
                    bundle_number=phone_number,
                    offer="40 cedis Bundle",
                    reference=client_ref,
                    transaction_status="Failed"
                )
                new_mtn_transaction.save()
                return redirect("failed")
    else:
        new_mtn_transaction = models.MTNBundleTransaction.objects.create(
            username=username,
            email=email,
            bundle_number=phone_number,
            offer="40 cedis Bundle",
            reference=client_ref,
            transaction_status="Failed"
        )
        new_mtn_transaction.save()
        print("last error")
        return redirect("failed")

######################################### 60 CEDI BUNDLE ######################################################

def pay_for_60_bundle(request):
    client_ref = 'gds'+str(random.randint(11111111, 99999999))

    if request.method == "POST":
        form = BundleForm(request.POST)
        if form.is_valid():
            phone_number = str(form.cleaned_data["phone"])
            amount = 60

            url = "https://payproxyapi.hubtel.com/items/initiate"

            payload = json.dumps({
            "totalAmount": amount,
            "description": "4.84GB Bundle",
            "callbackUrl": 'https://webhook.site/d53f5c53-eaba-4139-ad27-fb05b0a7be7f',
            "returnUrl": f'https://app.bestpaygh.com/send_60_mtn_bundle/{client_ref}/{phone_number}',
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
            return render(request, 'store/layouts/mtn_bundle.html', context={'form': form})
    else:
        form = BundleForm(initial={'phone':233})
    return render(request, "store/layouts/mtn_bundle.html", {'form': form})


def send_60_bundle(request, client_ref, phone_number, username, email):
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
            url = "https://cs.hubtel.com/commissionservices/2016884/b230733cd56b4a0fad820e39f66bc27c"

            payload = "{\r\n    \"Destination\": " + phone_number + ",\r\n    \"Amount\": 60.0,\r\n    \"CallbackUrl\": \"https://webhook.site/9125cb31-9481-47ad-972f-d1d7765a5957\",\r\n    \"ClientReference\": " + reference + ",\r\n    \"Extradata\" : {\r\n        \"bundle\" : \"flexi_data_bundle\"\r\n    }\r\n}\r\n"
            headers = {
                'Authorization': config("HUBTEL_API_KEY"),
                'Content-Type': 'text/plain'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            if response.status_code == 200:
                new_mtn_transaction = models.MTNBundleTransaction.objects.create(
                    username=username,
                    email=email,
                    bundle_number=phone_number,
                    offer="60 cedis Bundle",
                    reference=client_ref,
                    transaction_status="Success"
                )
                new_mtn_transaction.save()
                return redirect('thank_you')
            else:
                print("not 200 error")
                new_mtn_transaction = models.MTNBundleTransaction.objects.create(
                    username=username,
                    email=email,
                    bundle_number=phone_number,
                    offer="60 cedis Bundle",
                    reference=client_ref,
                    transaction_status="Failed"
                )
                new_mtn_transaction.save()
                return redirect("failed")
    else:
        new_mtn_transaction = models.MTNBundleTransaction.objects.create(
            username=username,
            email=email,
            bundle_number=phone_number,
            offer="60 cedis Bundle",
            reference=client_ref,
            transaction_status="Failed"
        )
        new_mtn_transaction.save()
        print("last error")
        return redirect("failed")

######################################### 80 CEDI BUNDLE ######################################################

def pay_for_80_bundle(request):
    client_ref = 'gds'+str(random.randint(11111111, 99999999))

    if request.method == "POST":
        form = BundleForm(request.POST)
        if form.is_valid():
            phone_number = str(form.cleaned_data["phone"])
            amount = 80

            url = "https://payproxyapi.hubtel.com/items/initiate"

            payload = json.dumps({
            "totalAmount": amount,
            "description": "6.45GB Bundle",
            "callbackUrl": 'https://webhook.site/d53f5c53-eaba-4139-ad27-fb05b0a7be7f',
            "returnUrl": f'https://app.bestpaygh.com/send_80_mtn_bundle/{client_ref}/{phone_number}',
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
            return render(request, 'store/layouts/mtn_bundle.html', context={'form': form})
    else:
        form = BundleForm(initial={'phone':233})
    return render(request, "store/layouts/mtn_bundle.html", {'form': form})


def send_80_bundle(request, client_ref, phone_number, username, email):
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
            url = "https://cs.hubtel.com/commissionservices/2016884/b230733cd56b4a0fad820e39f66bc27c"

            payload = "{\r\n    \"Destination\": " + phone_number + ",\r\n    \"Amount\": 80.0,\r\n    \"CallbackUrl\": \"https://webhook.site/9125cb31-9481-47ad-972f-d1d7765a5957\",\r\n    \"ClientReference\": " + reference + ",\r\n    \"Extradata\" : {\r\n        \"bundle\" : \"flexi_data_bundle\"\r\n    }\r\n}\r\n"
            headers = {
                'Authorization': config("HUBTEL_API_KEY"),
                'Content-Type': 'text/plain'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            if response.status_code == 200:
                new_mtn_transaction = models.MTNBundleTransaction.objects.create(
                    username=username,
                    email=email,
                    bundle_number=phone_number,
                    offer="80 cedis Bundle",
                    reference=client_ref,
                    transaction_status="Success"
                )
                new_mtn_transaction.save()
                return redirect('thank_you')
            else:
                print("not 200 error")
                new_mtn_transaction = models.MTNBundleTransaction.objects.create(
                    username=username,
                    email=email,
                    bundle_number=phone_number,
                    offer="80 cedis Bundle",
                    reference=client_ref,
                    transaction_status="Failed"
                )
                new_mtn_transaction.save()
                return redirect("failed")
    else:
        new_mtn_transaction = models.MTNBundleTransaction.objects.create(
            username=username,
            email=email,
            bundle_number=phone_number,
            offer="80 cedis Bundle",
            reference=client_ref,
            transaction_status="Failed"
        )
        new_mtn_transaction.save()
        print("last error")
        return redirect("failed")

######################################### 100 CEDI BUNDLE ######################################################

def pay_for_100_bundle(request):
    client_ref = 'gds'+str(random.randint(11111111, 99999999))

    if request.method == "POST":
        form = BundleForm(request.POST)
        if form.is_valid():
            phone_number = str(form.cleaned_data["phone"])
            amount = 100

            url = "https://payproxyapi.hubtel.com/items/initiate"

            payload = json.dumps({
            "totalAmount": amount,
            "description": "10.64GB Bundle",
            "callbackUrl": 'https://webhook.site/d53f5c53-eaba-4139-ad27-fb05b0a7be7f',
            "returnUrl": f'https://app.bestpaygh.com/send_100_mtn_bundle/{client_ref}/{phone_number}',
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
            return render(request, 'store/layouts/mtn_bundle.html', context={'form': form})
    else:
        form = BundleForm(initial={'phone':233})
    return render(request, "store/layouts/mtn_bundle.html", {'form': form})


def send_100_bundle(request, client_ref, phone_number, username, email):
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
            url = "https://cs.hubtel.com/commissionservices/2016884/b230733cd56b4a0fad820e39f66bc27c"

            payload = "{\r\n    \"Destination\": " + phone_number + ",\r\n    \"Amount\": 100.0,\r\n    \"CallbackUrl\": \"https://webhook.site/9125cb31-9481-47ad-972f-d1d7765a5957\",\r\n    \"ClientReference\": " + reference + ",\r\n    \"Extradata\" : {\r\n        \"bundle\" : \"flexi_data_bundle\"\r\n    }\r\n}\r\n"
            headers = {
                'Authorization': config("HUBTEL_API_KEY"),
                'Content-Type': 'text/plain'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            if response.status_code == 200:
                new_mtn_transaction = models.MTNBundleTransaction.objects.create(
                    username=username,
                    email=email,
                    bundle_number=phone_number,
                    offer="100 cedis Bundle",
                    reference=client_ref,
                    transaction_status="Success"
                )
                new_mtn_transaction.save()
                return redirect('thank_you')
            else:
                print("not 200 error")
                new_mtn_transaction = models.MTNBundleTransaction.objects.create(
                    username=username,
                    email=email,
                    bundle_number=phone_number,
                    offer="100 cedis Bundle",
                    reference=client_ref,
                    transaction_status="Failed"
                )
                new_mtn_transaction.save()
                return redirect("failed")
    else:
        new_mtn_transaction = models.MTNBundleTransaction.objects.create(
            username=username,
            email=email,
            bundle_number=phone_number,
            offer="100 cedis Bundle",
            reference=client_ref,
            transaction_status="Failed"
        )
        new_mtn_transaction.save()
        print("last error")
        return redirect("failed")

######################################### 120 CEDI BUNDLE ######################################################

def pay_for_120_bundle(request):
    client_ref = 'gds'+str(random.randint(11111111, 99999999))

    if request.method == "POST":
        form = BundleForm(request.POST)
        if form.is_valid():
            phone_number = str(form.cleaned_data["phone"])
            amount = 120

            url = "https://payproxyapi.hubtel.com/items/initiate"

            payload = json.dumps({
            "totalAmount": amount,
            "description": "12.77GB Bundle",
            "callbackUrl": 'https://webhook.site/d53f5c53-eaba-4139-ad27-fb05b0a7be7f',
            "returnUrl": f'https://app.bestpaygh.com/send_120_mtn_bundle/{client_ref}/{phone_number}',
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
            return render(request, 'store/layouts/mtn_bundle.html', context={'form': form})
    else:
        form = BundleForm(initial={'phone':233})
    return render(request, "store/layouts/mtn_bundle.html", {'form': form})


def send_120_bundle(request, client_ref, phone_number, username, email):
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
            url = "https://cs.hubtel.com/commissionservices/2016884/b230733cd56b4a0fad820e39f66bc27c"

            payload = "{\r\n    \"Destination\": " + phone_number + ",\r\n    \"Amount\": 120.0,\r\n    \"CallbackUrl\": \"https://webhook.site/9125cb31-9481-47ad-972f-d1d7765a5957\",\r\n    \"ClientReference\": " + reference + ",\r\n    \"Extradata\" : {\r\n        \"bundle\" : \"flexi_data_bundle\"\r\n    }\r\n}\r\n"
            headers = {
                'Authorization': config("HUBTEL_API_KEY"),
                'Content-Type': 'text/plain'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            if response.status_code == 200:
                new_mtn_transaction = models.MTNBundleTransaction.objects.create(
                    username=username,
                    email=email,
                    bundle_number=phone_number,
                    offer="120 cedis Bundle",
                    reference=client_ref,
                    transaction_status="Success"
                )
                new_mtn_transaction.save()
                return redirect('thank_you')
            else:
                print("not 200 error")
                new_mtn_transaction = models.MTNBundleTransaction.objects.create(
                    username=username,
                    email=email,
                    bundle_number=phone_number,
                    offer="120 cedis Bundle",
                    reference=client_ref,
                    transaction_status="Failed"
                )
                new_mtn_transaction.save()
                return redirect("failed")
    else:
        new_mtn_transaction = models.MTNBundleTransaction.objects.create(
            username=username,
            email=email,
            bundle_number=phone_number,
            offer="120 cedis Bundle",
            reference=client_ref,
            transaction_status="Failed"
        )
        new_mtn_transaction.save()
        print("last error")
        return redirect("failed")

######################################### 150 CEDI BUNDLE ######################################################

def pay_for_150_bundle(request):
    client_ref = 'gds'+str(random.randint(11111111, 99999999))

    if request.method == "POST":
        form = BundleForm(request.POST)
        if form.is_valid():
            phone_number = str(form.cleaned_data["phone"])
            amount = 150

            url = "https://payproxyapi.hubtel.com/items/initiate"

            payload = json.dumps({
            "totalAmount": amount,
            "description": "15.96GB Bundle",
            "callbackUrl": 'https://webhook.site/d53f5c53-eaba-4139-ad27-fb05b0a7be7f',
            "returnUrl": f'https://app.bestpaygh.com/send_150_mtn_bundle/{client_ref}/{phone_number}',
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
            return render(request, 'store/layouts/mtn_bundle.html', context={'form': form})
    else:
        form = BundleForm(initial={'phone':233})
    return render(request, "store/layouts/mtn_bundle.html", {'form': form})


def send_150_bundle(request, client_ref, phone_number, username, email):
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
            url = "https://cs.hubtel.com/commissionservices/2016884/b230733cd56b4a0fad820e39f66bc27c"

            payload = "{\r\n    \"Destination\": " + phone_number + ",\r\n    \"Amount\": 150.0,\r\n    \"CallbackUrl\": \"https://webhook.site/9125cb31-9481-47ad-972f-d1d7765a5957\",\r\n    \"ClientReference\": " + reference + ",\r\n    \"Extradata\" : {\r\n        \"bundle\" : \"flexi_data_bundle\"\r\n    }\r\n}\r\n"
            headers = {
                'Authorization': config("HUBTEL_API_KEY"),
                'Content-Type': 'text/plain'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            if response.status_code == 200:
                new_mtn_transaction = models.MTNBundleTransaction.objects.create(
                    username=username,
                    email=email,
                    bundle_number=phone_number,
                    offer="150 cedis Bundle",
                    reference=client_ref,
                    transaction_status="Success"
                )
                new_mtn_transaction.save()
                return redirect('thank_you')
            else:
                print("not 200 error")
                new_mtn_transaction = models.MTNBundleTransaction.objects.create(
                    username=username,
                    email=email,
                    bundle_number=phone_number,
                    offer="150 cedis Bundle",
                    reference=client_ref,
                    transaction_status="Failed"
                )
                new_mtn_transaction.save()
                return redirect("failed")
    else:
        new_mtn_transaction = models.MTNBundleTransaction.objects.create(
            username=username,
            email=email,
            bundle_number=phone_number,
            offer="150 cedis Bundle",
            reference=client_ref,
            transaction_status="Failed"
        )
        new_mtn_transaction.save()
        print("last error")
        return redirect("failed")

######################################### 200 CEDI BUNDLE ######################################################

def pay_for_200_bundle(request):
    client_ref = 'gds'+str(random.randint(11111111, 99999999))

    if request.method == "POST":
        form = BundleForm(request.POST)
        if form.is_valid():
            phone_number = str(form.cleaned_data["phone"])
            amount = 200

            url = "https://payproxyapi.hubtel.com/items/initiate"

            payload = json.dumps({
            "totalAmount": amount,
            "description": "35.84GB Bundle",
            "callbackUrl": 'https://webhook.site/d53f5c53-eaba-4139-ad27-fb05b0a7be7f',
            "returnUrl": f'https://app.bestpaygh.com/send_200_mtn_bundle/{client_ref}/{phone_number}',
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
            return render(request, 'store/layouts/mtn_bundle.html', context={'form': form})
    else:
        form = BundleForm(initial={'phone':233})
    return render(request, "store/layouts/mtn_bundle.html", {'form': form})


def send_200_bundle(request, client_ref, phone_number, username, email):
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
            url = "https://cs.hubtel.com/commissionservices/2016884/b230733cd56b4a0fad820e39f66bc27c"

            payload = "{\r\n    \"Destination\": " + phone_number + ",\r\n    \"Amount\": 200.0,\r\n    \"CallbackUrl\": \"https://webhook.site/9125cb31-9481-47ad-972f-d1d7765a5957\",\r\n    \"ClientReference\": " + reference + ",\r\n    \"Extradata\" : {\r\n        \"bundle\" : \"flexi_data_bundle\"\r\n    }\r\n}\r\n"
            headers = {
                'Authorization': config("HUBTEL_API_KEY"),
                'Content-Type': 'text/plain'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            if response.status_code == 200:
                new_mtn_transaction = models.MTNBundleTransaction.objects.create(
                    username=username,
                    email=email,
                    bundle_number=phone_number,
                    offer="200 cedis Bundle",
                    reference=client_ref,
                    transaction_status="Success"
                )
                new_mtn_transaction.save()
                return redirect('thank_you')
            else:
                print("not 200 error")
                new_mtn_transaction = models.MTNBundleTransaction.objects.create(
                    username=username,
                    email=email,
                    bundle_number=phone_number,
                    offer="200 cedis Bundle",
                    reference=client_ref,
                    transaction_status="Failed"
                )
                new_mtn_transaction.save()
                return redirect("failed")
    else:
        new_mtn_transaction = models.MTNBundleTransaction.objects.create(
            username=username,
            email=email,
            bundle_number=phone_number,
            offer="200 cedis Bundle",
            reference=client_ref,
            transaction_status="Failed"
        )
        new_mtn_transaction.save()
        print("last error")
        return redirect("failed")

######################################### 250 CEDI BUNDLE ######################################################

def pay_for_250_bundle(request):
    client_ref = 'gds'+str(random.randint(11111111, 99999999))

    if request.method == "POST":
        form = BundleForm(request.POST)
        if form.is_valid():
            phone_number = str(form.cleaned_data["phone"])
            amount = 250

            url = "https://payproxyapi.hubtel.com/items/initiate"

            payload = json.dumps({
            "totalAmount": amount,
            "description": "44.80GB Bundle",
            "callbackUrl": 'https://webhook.site/d53f5c53-eaba-4139-ad27-fb05b0a7be7f',
            "returnUrl": f'https://app.bestpaygh.com/send_250_mtn_bundle/{client_ref}/{phone_number}',
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
            return render(request, 'store/layouts/mtn_bundle.html', context={'form': form})
    else:
        form = BundleForm(initial={'phone':233})
    return render(request, "store/layouts/mtn_bundle.html", {'form': form})


def send_250_bundle(request, client_ref, phone_number, username, email):
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
            url = "https://cs.hubtel.com/commissionservices/2016884/b230733cd56b4a0fad820e39f66bc27c"

            payload = "{\r\n    \"Destination\": " + phone_number + ",\r\n    \"Amount\": 250.0,\r\n    \"CallbackUrl\": \"https://webhook.site/9125cb31-9481-47ad-972f-d1d7765a5957\",\r\n    \"ClientReference\": " + reference + ",\r\n    \"Extradata\" : {\r\n        \"bundle\" : \"flexi_data_bundle\"\r\n    }\r\n}\r\n"
            headers = {
                'Authorization': config("HUBTEL_API_KEY"),
                'Content-Type': 'text/plain'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            if response.status_code == 200:
                new_mtn_transaction = models.MTNBundleTransaction.objects.create(
                    username=username,
                    email=email,
                    bundle_number=phone_number,
                    offer="250 cedis Bundle",
                    reference=client_ref,
                    transaction_status="Success"
                )
                new_mtn_transaction.save()
                return redirect('thank_you')
            else:
                print("not 200 error")
                new_mtn_transaction = models.MTNBundleTransaction.objects.create(
                    username=username,
                    email=email,
                    bundle_number=phone_number,
                    offer="250 cedis Bundle",
                    reference=client_ref,
                    transaction_status="Failed"
                )
                new_mtn_transaction.save()
                return redirect("failed")
    else:
        new_mtn_transaction = models.MTNBundleTransaction.objects.create(
            username=username,
            email=email,
            bundle_number=phone_number,
            offer="250 cedis Bundle",
            reference=client_ref,
            transaction_status="Failed"
        )
        new_mtn_transaction.save()
        print("last error")
        return redirect("failed")

######################################### 299 CEDI BUNDLE ######################################################

def pay_for_300_bundle(request):
    client_ref = 'gds'+str(random.randint(11111111, 99999999))

    if request.method == "POST":
        form = BundleForm(request.POST)
        if form.is_valid():
            phone_number = str(form.cleaned_data["phone"])
            amount = 300

            url = "https://payproxyapi.hubtel.com/items/initiate"

            payload = json.dumps({
            "totalAmount": amount,
            "description": "53.58GB Bundle",
            "callbackUrl": 'https://webhook.site/d53f5c53-eaba-4139-ad27-fb05b0a7be7f',
            "returnUrl": f'https://app.bestpaygh.com/send_300_mtn_bundle/{client_ref}/{phone_number}',
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
            return render(request, 'store/layouts/mtn_bundle.html', context={'form': form})
    else:
        form = BundleForm(initial={'phone':233})
    return render(request, "store/layouts/mtn_bundle.html", {'form': form})


def send_300_bundle(request, client_ref, phone_number, username, email):
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
            url = "https://cs.hubtel.com/commissionservices/2016884/b230733cd56b4a0fad820e39f66bc27c"

            payload = "{\r\n    \"Destination\": " + phone_number + ",\r\n    \"Amount\": 300.0,\r\n    \"CallbackUrl\": \"https://webhook.site/9125cb31-9481-47ad-972f-d1d7765a5957\",\r\n    \"ClientReference\": " + reference + ",\r\n    \"Extradata\" : {\r\n        \"bundle\" : \"flexi_data_bundle\"\r\n    }\r\n}\r\n"
            headers = {
                'Authorization': config("HUBTEL_API_KEY"),
                'Content-Type': 'text/plain'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            if response.status_code == 200:
                new_mtn_transaction = models.MTNBundleTransaction.objects.create(
                    username=username,
                    email=email,
                    bundle_number=phone_number,
                    offer="300 cedis Bundle",
                    reference=client_ref,
                    transaction_status="Success"
                )
                new_mtn_transaction.save()
                return redirect('thank_you')
            else:
                print("not 200 error")
                new_mtn_transaction = models.MTNBundleTransaction.objects.create(
                    username=username,
                    email=email,
                    bundle_number=phone_number,
                    offer="300 cedis Bundle",
                    reference=client_ref,
                    transaction_status="Failed"
                )
                new_mtn_transaction.save()
                return redirect("failed")
    else:
        new_mtn_transaction = models.MTNBundleTransaction.objects.create(
            username=username,
            email=email,
            bundle_number=phone_number,
            offer="300 cedis Bundle",
            reference=client_ref,
            transaction_status="Failed"
        )
        new_mtn_transaction.save()
        print("last error")
        return redirect("failed")


######################################### 400 CEDI BUNDLE ######################################################

def pay_for_400_bundle(request):
    client_ref = 'gds'+str(random.randint(11111111, 99999999))

    if request.method == "POST":
        form = BundleForm(request.POST)
        if form.is_valid():
            phone_number = str(form.cleaned_data["phone"])
            amount = 400

            url = "https://payproxyapi.hubtel.com/items/initiate"

            payload = json.dumps({
            "totalAmount": amount,
            "description": "53.58GB Bundle",
            "callbackUrl": 'https://webhook.site/d53f5c53-eaba-4139-ad27-fb05b0a7be7f',
            "returnUrl": f'https://app.bestpaygh.com/send_400_mtn_bundle/{client_ref}/{phone_number}',
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
            return render(request, 'store/layouts/mtn_bundle.html', context={'form': form})
    else:
        form = BundleForm(initial={'phone':233})
    return render(request, "store/layouts/mtn_bundle.html", {'form': form})


def send_400_bundle(request, client_ref, phone_number, username, email):
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
            url = "https://cs.hubtel.com/commissionservices/2016884/b230733cd56b4a0fad820e39f66bc27c"

            payload = "{\r\n    \"Destination\": " + phone_number + ",\r\n    \"Amount\": 400.0,\r\n    \"CallbackUrl\": \"https://webhook.site/9125cb31-9481-47ad-972f-d1d7765a5957\",\r\n    \"ClientReference\": " + reference + ",\r\n    \"Extradata\" : {\r\n        \"bundle\" : \"flexi_data_bundle\"\r\n    }\r\n}\r\n"
            headers = {
                'Authorization': config("HUBTEL_API_KEY"),
                'Content-Type': 'text/plain'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            if response.status_code == 200:
                new_mtn_transaction = models.MTNBundleTransaction.objects.create(
                    username=username,
                    email=email,
                    bundle_number=phone_number,
                    offer="400 cedis Bundle",
                    reference=client_ref,
                    transaction_status="Success"
                )
                new_mtn_transaction.save()
                return redirect('thank_you')
            else:
                print("not 200 error")
                new_mtn_transaction = models.MTNBundleTransaction.objects.create(
                    username=username,
                    email=email,
                    bundle_number=phone_number,
                    offer="400 cedis Bundle",
                    reference=client_ref,
                    transaction_status="Failed"
                )
                new_mtn_transaction.save()
                return redirect("failed")
    else:
        new_mtn_transaction = models.MTNBundleTransaction.objects.create(
            username=username,
            email=email,
            bundle_number=phone_number,
            offer="400 cedis Bundle",
            reference=client_ref,
            transaction_status="Failed"
        )
        new_mtn_transaction.save()
        print("last error")
        return redirect("failed")

############################################ Kokrooko ############################################3


def pay_for_k1_bundle(request):
    client_ref = 'gds'+str(random.randint(11111111, 99999999))

    if request.method == "POST":
        form = BundleForm(request.POST)
        if form.is_valid():
            phone_number = str(form.cleaned_data["phone"])
            amount = 0.99

            url = "https://payproxyapi.hubtel.com/items/initiate"

            payload = json.dumps({
            "totalAmount": amount,
            "description": "Kokrokoo 400MB, 20Min",
            "callbackUrl": 'https://webhook.site/d53f5c53-eaba-4139-ad27-fb05b0a7be7f',
            "returnUrl": f'https://app.bestpaygh.com/send_k1_mtn_bundle/{client_ref}/{phone_number}',
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
            return render(request, 'store/layouts/mtn_bundle.html', context={'form': form})
    else:
        form = BundleForm(initial={'phone':233})
    return render(request, "store/layouts/mtn_bundle.html", {'form': form})


def send_k1_bundle(request, client_ref, phone_number, username, email):
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
            url = "https://cs.hubtel.com/commissionservices/2016884/b230733cd56b4a0fad820e39f66bc27c"

            payload = "{\r\n    \"Destination\": " + phone_number + ",\r\n    \"Amount\": 1.09,\r\n    \"CallbackUrl\": \"https://webhook.site/9125cb31-9481-47ad-972f-d1d7765a5957\",\r\n    \"ClientReference\": " + reference + ",\r\n    \"Extradata\" : {\r\n        \"bundle\" : \"kokrokoo_bundle_1\"\r\n    }\r\n}\r\n"
            headers = {
                'Authorization': config("HUBTEL_API_KEY"),
                'Content-Type': 'text/plain'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            if response.status_code == 200:
                new_mtn_transaction = models.OtherMTNBundleTransaction.objects.create(
                    username=username,
                    email=email,
                    bundle_number=phone_number,
                    offer="Kokrooko",
                    reference=client_ref,
                    transaction_status="Success"
                )
                new_mtn_transaction.save()
                return redirect('thank_you')
            else:
                print("not 200 error")
                new_mtn_transaction = models.OtherMTNBundleTransaction.objects.create(
                    username=username,
                    email=email,
                    bundle_number=phone_number,
                    offer="Kokrooko",
                    reference=client_ref,
                    transaction_status="Failed"
                )
                new_mtn_transaction.save()
                return redirect("failed")
    else:
        new_mtn_transaction = models.OtherMTNBundleTransaction.objects.create(
            username=username,
            email=email,
            bundle_number=phone_number,
            offer="Kokrooko",
            reference=client_ref,
            transaction_status="Failed"
        )
        new_mtn_transaction.save()
        print("last error")
        return redirect("failed")


