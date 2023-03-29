import datetime
import secrets
from django.shortcuts import render, redirect, reverse
import requests

from datashop import models
from .forms import AirtimeForm
from django.contrib import messages
import json
from django.http import HttpResponse
import random
from decouple import config


def ref_generator(number):
    now_time = datetime.datetime.now().strftime('%H%M%S')
    secret = secrets.token_hex(number)

    return f"ABP{now_time}{secret}".upper()

# Create your views here.
def mtn_request(request):
    client_ref = ref_generator(2)

    if request.method == 'POST':
        form = AirtimeForm(request.POST)
        if form.is_valid():
            phone = str(form.cleaned_data['phone'])
            amount = str(form.cleaned_data['amount'])

            amount_to_be_charged = amount

            float_amount = float(amount)
            if float_amount == 0.5:
                amount_to_be_charged = 0.49
            elif float_amount == 1.00:
                percentage = 0.01
                amount_to_be_charged = float_amount - percentage
            elif float_amount >= 2 and float_amount <= 10:
                percentage = 0.10
                amount_to_be_charged = float_amount - percentage
            elif float_amount >= 11 and float_amount <= 50:
                percentage = 0.50
                amount_to_be_charged = float_amount - percentage       

            url = "https://payproxyapi.hubtel.com/items/initiate"

            payload = json.dumps({
            "totalAmount": amount_to_be_charged,
            "description": "Test",
            "callbackUrl": 'https://webhook.site/d53f5c53-eaba-4139-ad27-fb05b0a7be7f',
            "returnUrl": f'http://app.bestpaygh.com/send_airtime_mtn/{client_ref}/{phone}/{amount}/mike/mike@mike.com',
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
            return render(request, 'store/layouts/mtn.html', context={'form': form})
    else:
        form = AirtimeForm()
    return render(request, 'store/layouts/mtn.html', context={'form': form})


def send_airtime_mtn(request, client_ref, phone, amount, username, email):
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
    webhook_response = requests.request("GET", "https://webhook.site/token/d53f5c53-eaba-4139-ad27-fb05b0a7be7f/requests?sorting=newest", headers=headers)
    
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
        amount = content_needed["Data"]["Amount"]
        payment_description = content_needed["Data"]["Description"]
        print(f"{status_needed}--{ref_needed}--{momo_number}--{amount}--{payment_description}")
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
                amount=amount,
                payment_description=payment_description,
                transaction_status=status_needed,
                payment_visited=True,
                message="Payment verified successfully",
            )
            new_payment.save()    


            mtn_url = "https://cs.hubtel.com/commissionservices/2016884/fdd76c884e614b1c8f669a3207b09a98"

            reference = f"\"{client_ref}\""

            payload = "{\r\n    \"Destination\": " + str(phone) + ",\r\n    \"Amount\": " + str(amount) + ",\r\n    \"CallbackUrl\": \"https://webhook.site/9125cb31-9481-47ad-972f-d1d7765a5957\",\r\n    \"ClientReference\": " + str(reference) + "\r\n}"
                        
            headers = {
                'Authorization': config("HUBTEL_API_KEY"),
                'Content-Type': 'text/plain'
            }

            response = requests.request("POST", mtn_url, headers=headers, data=payload)

            airtime_data = response.json()
            print(airtime_data)
            print(response.status_code)

            if response.status_code == 200:
                new_airtime_transaction = models.AirtimeTransaction.objects.create(
                    username=username,
                    email=email,
                    airtime_number=phone,
                    airtime_amount=amount,
                    provider="MTN",
                    reference=client_ref,
                    transaction_status="Success"
                )
                new_airtime_transaction.save()
                return redirect('thank_you')
            else:
                print("not 200 error")
                new_airtime_transaction = models.AirtimeTransaction.objects.create(
                    username=username,
                    email=email,
                    airtime_number=phone,
                    airtime_amount=amount,
                    provider="MTN",
                    reference=reference,
                    transaction_status="Failed"
                )
                new_airtime_transaction.save()
                return redirect("failed")
    else:
        new_airtime_transaction = models.AirtimeTransaction.objects.create(
            username=username,
            email=email,
            airtime_number=phone,
            airtime_amount=amount,
            provider="MTN",
            reference=client_ref,
            transaction_status="Failed"
        )
        new_airtime_transaction.save()
        print("last error")
        return redirect("failed")            
                    

def voda_request(request):
    client_ref = 'gds'+str(random.randint(11111111, 99999999))

    if request.method == 'POST':
        form = AirtimeForm(request.POST)
        if form.is_valid():
            phone = str(form.cleaned_data['phone'])
            amount = str(form.cleaned_data['amount'])

            amount_to_be_charged = amount

            float_amount = float(amount)
            if float_amount == 0.5:
                amount_to_be_charged = 0.49
            elif float_amount == 1.00:
                percentage = 0.01
                amount_to_be_charged = float_amount - percentage
            elif 2 <= float_amount <= 10:
                percentage = 0.10
                amount_to_be_charged = float_amount - percentage
            elif 11 <= float_amount <= 50:
                percentage = 0.50
                amount_to_be_charged = float_amount - percentage 

            url = "https://payproxyapi.hubtel.com/items/initiate"

            payload = json.dumps({
                "totalAmount": amount_to_be_charged,
                "description": "Test",
                "callbackUrl": 'https://webhook.site/d53f5c53-eaba-4139-ad27-fb05b0a7be7f',
                "returnUrl": f'https://app.bestpaygh.com/send_airtime_voda/{client_ref}/{phone}/{amount}',
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
                messages.info(request, "Successful")
                checkout = data['data']['checkoutUrl']
                return redirect(checkout)
            else:
                messages.info(request, "Failed. Try again later")
            return render(request, 'store/layouts/voda.html', context={'form': form})
    else:
        form = AirtimeForm(initial={'phone':233})
    return render(request, 'store/layouts/voda.html', context={'form': form})


def send_airtime_voda(request, client_ref, phone, amount, username, email):
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
    webhook_response = requests.request("GET", "https://webhook.site/token/d53f5c53-eaba-4139-ad27-fb05b0a7be7f/requests?sorting=newest", headers=headers)
    
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

            voda_url = "https://cs.hubtel.com/commissionservices/2016884/f4be83ad74c742e185224fdae1304800"

            payload = "{\r\n    \"Destination\": " + str(phone) + ",\r\n    \"Amount\": " + str(amount) + ",\r\n    \"CallbackUrl\": \"https://webhook.site/9125cb31-9481-47ad-972f-d1d7765a5957\",\r\n    \"ClientReference\": " + str(reference) + "\r\n}"
                        
            headers = {
                'Authorization': config("HUBTEL_API_KEY"),
                'Content-Type': 'text/plain'
            }

            response = requests.request("POST", voda_url, headers=headers, data=payload)

            if response.status_code == 200:
                new_airtime_transaction = models.AirtimeTransaction.objects.create(
                    username=username,
                    email=email,
                    airtime_number=phone,
                    airtime_amount=amount,
                    provider="Vodafone",
                    reference=client_ref,
                    transaction_status="Success"
                )
                new_airtime_transaction.save()
                return redirect('thank_you')
            else:
                print("not 200 error")
                new_airtime_transaction = models.AirtimeTransaction.objects.create(
                    username=username,
                    email=email,
                    airtime_number=phone,
                    airtime_amount=amount,
                    provider="Vodafone",
                    reference=reference,
                    transaction_status="Failed"
                )
                new_airtime_transaction.save()
                return redirect("failed")
    else:
        new_airtime_transaction = models.AirtimeTransaction.objects.create(
            username=username,
            email=email,
            airtime_number=phone,
            airtime_amount=amount,
            provider="Vodafone",
            reference=client_ref,
            transaction_status="Failed"
        )
        new_airtime_transaction.save()
        print("last error")
        return redirect("failed")


def airtel_tigo_request(request):
    client_ref = 'gds'+str(random.randint(11111111, 99999999))

    if request.method == 'POST':
        form = AirtimeForm(request.POST)
        if form.is_valid():
            phone = str(form.cleaned_data['phone'])
            amount = str(form.cleaned_data['amount'])

            amount_to_be_charged = amount

            float_amount = float(amount)
            if float_amount == 0.5:
                amount_to_be_charged = 0.49
            elif float_amount == 1.00:
                percentage = 0.01
                amount_to_be_charged = float_amount - percentage
            elif 2 <= float_amount <= 10:
                percentage = 0.10
                amount_to_be_charged = float_amount - percentage
            elif 11 <= float_amount <= 50:
                percentage = 0.50
                amount_to_be_charged = float_amount - percentage 

            url = "https://payproxyapi.hubtel.com/items/initiate"

            payload = json.dumps({
                "totalAmount": amount_to_be_charged,
                "description": "Test",
                "callbackUrl": 'https://webhook.site/d53f5c53-eaba-4139-ad27-fb05b0a7be7f',
                "returnUrl": f'https://app.bestpaygh.com/send_airtime_tigo/{client_ref}/{phone}/{amount}',
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
                messages.info(request, "Successful")
                checkout = data['data']['checkoutUrl']
                return redirect(checkout)
            else:
                messages.info(request, "Failed. Try again later")
            return render(request, 'store/layouts/tigo.html', context={'form': form})
    else:
        form = AirtimeForm(initial={'phone':233})
    return render(request, 'store/layouts/tigo.html', context={'form': form})


def send_airtime_tigo(request, client_ref, phone, amount, username, email):
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
        print(f"{status_needed}--{ref_needed}--{momo_number}--{amount}--{payment_description}")
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

            tigo_url = "https://cs.hubtel.com/commissionservices/2016884/dae2142eb5a14c298eace60240c09e4b"

            payload = "{\r\n    \"Destination\": " + str(phone) + ",\r\n    \"Amount\": " + str(amount) + ",\r\n    \"CallbackUrl\": \"https://webhook.site/9125cb31-9481-47ad-972f-d1d7765a5957\",\r\n    \"ClientReference\": " + reference + "\r\n}"
                    
            airtime_headers = {
                'Authorization': config("HUBTEL_API_KEY"),
                'Content-Type': 'text/plain'
            }

            response = requests.request("POST", tigo_url, headers=airtime_headers, data=payload)

            if response.status_code == 200:
                new_airtime_transaction = models.AirtimeTransaction.objects.create(
                    username=username,
                    email=email,
                    airtime_number=phone,
                    airtime_amount=amount,
                    provider="AirtelTigo",
                    reference=client_ref,
                    transaction_status="Success"
                )
                new_airtime_transaction.save()
                return redirect('thank_you')
            else:
                print("not 200 error")
                new_airtime_transaction = models.AirtimeTransaction.objects.create(
                    username=username,
                    email=email,
                    airtime_number=phone,
                    airtime_amount=amount,
                    provider="AirtelTigo",
                    reference=reference,
                    transaction_status="Failed"
                )
                new_airtime_transaction.save()
                return redirect("failed")
    else:
        new_airtime_transaction = models.AirtimeTransaction.objects.create(
            username=username,
            email=email,
            airtime_number=phone,
            airtime_amount=amount,
            provider="Vodafone",
            reference=client_ref,
            transaction_status="Failed"
        )
        new_airtime_transaction.save()
        print("last error")
        return redirect("failed")


def glo_request(request):
    client_ref = 'gds'+str(random.randint(11111111, 99999999))

    if request.method == 'POST':
        form = AirtimeForm(request.POST)
        if form.is_valid():
            phone = str(form.cleaned_data['phone'])
            amount = str(form.cleaned_data['amount'])

            amount_to_be_charged = amount

            float_amount = float(amount)
            if float_amount == 0.5:
                amount_to_be_charged = 0.49
            if float_amount == 1.00:
                percentage = 0.01
                amount_to_be_charged = float_amount - percentage
            elif 2 <= float_amount <= 10:
                percentage = 0.10
                amount_to_be_charged = float_amount - percentage
            elif 11 <= float_amount <= 50:
                percentage = 0.50
                amount_to_be_charged = float_amount - percentage 

            url = "https://payproxyapi.hubtel.com/items/initiate"

            payload = json.dumps({
                "totalAmount": amount_to_be_charged,
                "description": "Test",
                "callbackUrl": 'https://webhook.site/d53f5c53-eaba-4139-ad27-fb05b0a7be7f',
                "returnUrl": f'https://app.bestpaygh.com/send_airtime_glo/{client_ref}/{phone}/{amount}',
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
                messages.info(request, "Successful")
                checkout = data['data']['checkoutUrl']
                return redirect(checkout)
            else:
                messages.info(request, "Failed. Try again later")
            return render(request, 'store/layouts/glo.html', context={'form': form})
    else:
        form = AirtimeForm(initial={'phone':233})
    return render(request, 'store/layouts/glo.html', context={'form': form})


def send_airtime_glo(request, client_ref, phone, amount, username, email):
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
        print(f"{status_needed}--{ref_needed}--{momo_number}--{amount}--{payment_description}")
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
            glo_url = "https://cs.hubtel.com/commissionservices/2016884/47d88e88f50f47468a34a14ac73e8ab5"

            payload = "{\r\n    \"Destination\": " + phone + ",\r\n    \"Amount\": " + amount + ",\r\n    \"CallbackUrl\": \"https://webhook.site/9125cb31-9481-47ad-972f-d1d7765a5957\",\r\n    \"ClientReference\": " + reference  + "\r\n}"
                    
            airtime_headers = {
                'Authorization': config("HUBTEL_API_KEY"),
                'Content-Type': 'text/plain'
            }

            response = requests.request("POST", glo_url, headers=airtime_headers, data=payload)

            if response.status_code == 200:
                new_airtime_transaction = models.AirtimeTransaction.objects.create(
                    username=username,
                    email=email,
                    airtime_number=phone,
                    airtime_amount=amount,
                    provider="Glo",
                    reference=client_ref,
                    transaction_status="Success"
                )
                new_airtime_transaction.save()
                return redirect('thank_you')
            else:
                print("not 200 error")
                new_airtime_transaction = models.AirtimeTransaction.objects.create(
                    username=username,
                    email=email,
                    airtime_number=phone,
                    airtime_amount=amount,
                    provider="Glo",
                    reference=reference,
                    transaction_status="Failed"
                )
                new_airtime_transaction.save()
                return redirect("failed")
    else:
        new_airtime_transaction = models.AirtimeTransaction.objects.create(
            username=username,
            email=email,
            airtime_number=phone,
            airtime_amount=amount,
            provider="Glo",
            reference=client_ref,
            transaction_status="Failed"
        )
        new_airtime_transaction.save()
        print("last error")
        return redirect("failed")
                    

def thank_you(request):
    return render(request, "store/layouts/thanks.html")


def failed(request):
    return render(request, "store/layouts/failed.html")


def intruder(request):
    return render(request, "store/layouts/intruder.html")


def send_sms(request, reference, receiver, user_phone, amount):
    sms_message = f"{reference} receiver of {amount} for {receiver}  ==> {user_phone}"
    sms_url = f"https://sms.arkesel.com/sms/api?action=send-sms&api_key=UmpEc1JzeFV4cERKTWxUWktqZEs&to=0592117523&from=BP Order&sms={sms_message}"
    response = requests.request("GET", url=sms_url)
    print(response.status_code)
    return HttpResponse('')
                
