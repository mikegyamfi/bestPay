from django.shortcuts import render, redirect, reverse
import requests
from .forms import AirtimeForm
from django.contrib import messages
import json
from django.http import HttpResponse
import random

# Create your views here.
def mtn_request(request):
    client_ref = 'gds'+str(random.randint(11111111, 99999999))

    if request.method == 'POST':
        form = AirtimeForm(request.POST)
        if form.is_valid():
            phone = str(form.cleaned_data['phone'])
            amount = str(form.cleaned_data['amount'])

            percentage = 0.01 * double(amount)
            amount_to_be_paid = amount - percentage

            url = "https://payproxyapi.hubtel.com/items/initiate"

            payload = json.dumps({
            "totalAmount": amount_to_be_paid,
            "description": "Test",
            "callbackUrl": 'https://webhook.site/092193ad-e5e7-4f17-a472-3442a8670569',
            "returnUrl": f'https://bestpay-app-id6nm.ondigitalocean.app/send_airtime_mtn/{client_ref}/{phone}/{amount}',
            "cancellationUrl": "https://www.google.com",
            "merchantAccountNumber": "2017101",
            "clientReference": client_ref
            })
            headers = {
            'Authorization': 'Basic VnY3MHhuTTplNTAzYzcyMGYzYzA0N2Q2ODNjYTM3MWQ5YWEwMDZkZg==',
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
            return render(request, 'store/layouts/mtn.html', context={'form': form})
    else:
        form = AirtimeForm()
    return render(request, 'store/layouts/mtn.html', context={'form': form})


def send_airtime_mtn(request, client_ref, phone, amount):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    webhook_response = requests.request("GET", "https://webhook.site/token/092193ad-e5e7-4f17-a472-3442a8670569/requests?sorting=newest", headers=headers)
    for request in webhook_response.json()['data']:
        content = json.loads(request["content"])
        status = content["Status"]
        ref = content["Data"]["ClientReference"]
        if ref == client_ref and status == "Success":
            mtn_url = "https://cs.hubtel.com/commissionservices/2016884/fdd76c884e614b1c8f669a3207b09a98"

            payload = "{\r\n    \"Destination\": " + phone + ",\r\n    \"Amount\": " + amount + ",\r\n    \"CallbackUrl\": \"https://webhook.site/092193ad-e5e7-4f17-a472-3442a8670569\",\r\n    \"ClientReference\": \"TestEVD01027\"\r\n}"
                    
            headers = {
                'Authorization': 'Basic VnY3MHhuTTplNTAzYzcyMGYzYzA0N2Q2ODNjYTM3MWQ5YWEwMDZkZg==',
                'Content-Type': 'text/plain'
            }

            response = requests.request("POST", mtn_url, headers=headers, data=payload)

            if response.status_code == 200:
                return redirect('thank_you')
            else:
                messages.info(request, "Try again Later")
                    

            return render(request, 'store/layouts/mtn.html', context={'form': form})

            break
            

def voda_request(request):
    client_ref = 'gds'+str(random.randint(11111111, 99999999))

    if request.method == 'POST':
        form = AirtimeForm(request.POST)
        if form.is_valid():
            phone = str(form.cleaned_data['phone'])
            amount = str(form.cleaned_data['amount'])

            url = "https://payproxyapi.hubtel.com/items/initiate"

            payload = json.dumps({
            "totalAmount": amount,
            "description": "Test",
            "callbackUrl": 'https://webhook.site/092193ad-e5e7-4f17-a472-3442a8670569',
            "returnUrl": f'https://bestpay-app-id6nm.ondigitalocean.app/send_airtime_voda/{client_ref}/{phone}/{amount}',
            "cancellationUrl": "https://www.google.com",
            "merchantAccountNumber": "2017101",
            "clientReference": client_ref
            })
            headers = {
            'Authorization': 'Basic VnY3MHhuTTplNTAzYzcyMGYzYzA0N2Q2ODNjYTM3MWQ5YWEwMDZkZg==',
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
        form = AirtimeForm()
    return render(request, 'store/layouts/voda.html', context={'form': form})


def send_airtime_voda(request, client_ref, phone, amount):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    webhook_response = requests.request("GET", "https://webhook.site/token/092193ad-e5e7-4f17-a472-3442a8670569/requests?sorting=newest", headers=headers)
    for request in webhook_response.json()['data']:
        content = json.loads(request["content"])
        status = content["Status"]
        ref = content["Data"]["ClientReference"]
        if ref == client_ref and status == "Success":
            voda_url = "https://cs.hubtel.com/commissionservices/2016884/f4be83ad74c742e185224fdae1304800"

            payload = "{\r\n    \"Destination\": " + phone + ",\r\n    \"Amount\": " + amount + ",\r\n    \"CallbackUrl\": \"https://webhook.site/092193ad-e5e7-4f17-a472-3442a8670569\",\r\n    \"ClientReference\": \"TestEVD01027\"\r\n}"
                    
            headers = {
                'Authorization': 'Basic VnY3MHhuTTplNTAzYzcyMGYzYzA0N2Q2ODNjYTM3MWQ5YWEwMDZkZg==',
                'Content-Type': 'text/plain'
            }

            response = requests.request("POST", voda_url, headers=headers, data=payload)

            if response.status_code == 200:
                return redirect('thank_you')
            else:
                messages.info(request, "Try again Later")
                    

            return render(request, 'store/layouts/voda.html', context={'form': form})

            break

def airtel_tigo_request(request):
    client_ref = 'gds'+str(random.randint(11111111, 99999999))

    if request.method == 'POST':
        form = AirtimeForm(request.POST)
        if form.is_valid():
            phone = str(form.cleaned_data['phone'])
            amount = str(form.cleaned_data['amount'])

            url = "https://payproxyapi.hubtel.com/items/initiate"

            payload = json.dumps({
            "totalAmount": amount,
            "description": "Test",
            "callbackUrl": 'https://webhook.site/092193ad-e5e7-4f17-a472-3442a8670569',
            "returnUrl": f'https://bestpay-app-id6nm.ondigitalocean.app/send_airtime_tigo/{client_ref}/{phone}/{amount}',
            "cancellationUrl": "https://www.google.com",
            "merchantAccountNumber": "2017101",
            "clientReference": client_ref
            })
            headers = {
            'Authorization': 'Basic VnY3MHhuTTplNTAzYzcyMGYzYzA0N2Q2ODNjYTM3MWQ5YWEwMDZkZg==',
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
        form = AirtimeForm()
    return render(request, 'store/layouts/tigo.html', context={'form': form})

def send_airtime_tigo(request, client_ref, phone, amount):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    webhook_response = requests.request("GET", "https://webhook.site/token/092193ad-e5e7-4f17-a472-3442a8670569/requests?sorting=newest", headers=headers)
    for request in webhook_response.json()['data']:
        content = json.loads(request["content"])
        status = content["Status"]
        ref = content["Data"]["ClientReference"]
        if ref == client_ref and status == "Success":
            tigo_url = "https://cs.hubtel.com/commissionservices/2016884/dae2142eb5a14c298eace60240c09e4b"

            payload = "{\r\n    \"Destination\": " + phone + ",\r\n    \"Amount\": " + amount + ",\r\n    \"CallbackUrl\": \"https://webhook.site/092193ad-e5e7-4f17-a472-3442a8670569\",\r\n    \"ClientReference\": \"TestEVD01027\"\r\n}"
                    
            airtime_headers = {
                'Authorization': 'Basic VnY3MHhuTTplNTAzYzcyMGYzYzA0N2Q2ODNjYTM3MWQ5YWEwMDZkZg==',
                'Content-Type': 'text/plain'
            }

            response = requests.request("POST", tigo_url, headers=airtime_headers, data=payload)

            if response.status_code == 200:
                return redirect('thank_you')
            else:
                messages.info(request, "Try again Later")
                    

            return render(request, 'store/layouts/tigo.html', context={'form': form})

            break


def thank_you(request):
    return render(request, "store/layouts/thanks.html")
