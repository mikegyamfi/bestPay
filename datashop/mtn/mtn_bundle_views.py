from django.shortcuts import render, redirect, reverse
import requests
from ..forms import BundleForm
from django.contrib import messages
import json
from django.http import HttpResponse
import random

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
            "returnUrl": f'https://bestpay-app-id6nm.ondigitalocean.app/send_50_mtn_bundle/{client_ref}/{phone_number}',
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
                checkout = data['data']['checkoutUrl']
                return redirect(checkout)
            else:
                messages.info(request, "Failed. Try again later")
            return render(request, 'store/layouts/mtn_bundle.html', context={'form': form})

    form = BundleForm()
    return render(request, "store/layouts/mtn_bundle.html", {'form': form})


def send_50p_bundle(request, client_ref, phone_number):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    webhook_response = requests.request("GET", "https://webhook.site/token/d53f5c53-eaba-4139-ad27-fb05b0a7be7f/requests?sorting=newest", headers=headers)

    for request in webhook_response.json()['data']:
        try:
            content = json.loads(request["content"])
            status = content["Status"]
            ref = content["Data"]["ClientReference"]
        except KeyError:
            return redirect("failed")
        if ref == client_ref and status == "Success":
            url = "https://cs.hubtel.com/commissionservices/2016884/b230733cd56b4a0fad820e39f66bc27c"

            payload = "{\r\n    \"Destination\": " + phone_number + ",\r\n    \"Amount\": 0.5,\r\n    \"CallbackUrl\": \"https://webhook.site/fcad8efa-624b-44c8-a129-b1c01921191d\",\r\n    \"ClientReference\": \"GHDS10001\",\r\n    \"Extradata\" : {\r\n        \"bundle\" : \"data_bundle_1\"\r\n    }\r\n}\r\n"
            headers = {
            'Authorization': 'Basic VnY3MHhuTTplNTAzYzcyMGYzYzA0N2Q2ODNjYTM3MWQ5YWEwMDZkZg==',
            'Content-Type': 'text/plain'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            if response.status_code == 200:
                return redirect('thank_you')
            else:
                return redirect("failed")
                    
            form = BundleForm()
            return render(request, 'store/layouts/mtn_bundle.html', context={'form': form})

            break