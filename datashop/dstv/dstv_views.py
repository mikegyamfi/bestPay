from django.shortcuts import render, redirect, reverse
import requests
from ..forms import TVForm
from django.contrib import messages
import json
from django.http import HttpResponse
import random
from decouple import config

def pay_for_dstv(request):
    client_ref = 'gds'+str(random.randint(11111111, 99999999))

    if request.method == "POST":
        form = TVForm(request.POST)
        if form.is_valid():
            account_number = str(form.cleaned_data["account_number"])
            amount = str(form.cleaned_data["amount"])

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
            "description": "GoTV",
            "callbackUrl": 'https://webhook.site/d53f5c53-eaba-4139-ad27-fb05b0a7be7f',
            "returnUrl": f'https://bestpay-app-id6nm.ondigitalocean.app/send_dstv_amount/{client_ref}/{account_number}/{amount}',
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
            return render(request, 'store/layouts/dstv.html', context={'form': form})
    else:
        form = TVForm()
    return render(request, "store/layouts/dstv.html", {'form': form})


def send_dstv_amount(request, client_ref, account_number, amount):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        "api-key": config('API_KEY')
    }
    webhook_response = requests.request("GET", "https://webhook.site/token/d53f5c53-eaba-4139-ad27-fb05b0a7be7f/requests?sorting=newest", headers=headers)

    for request in webhook_response.json()['data']:
        try:
            try:
                content = json.loads(request["content"])
            except ValueError:
                return redirect(f"https://bestpay-app-id6nm.ondigitalocean.app/send_dstv_amount/{client_ref}/{account_number}/{amount}")
            status = content["Status"]
            ref = content["Data"]["ClientReference"]
        except KeyError:
            return redirect("failed")
        if ref == client_ref and status == "Success":
            url = "https://cs.hubtel.com/commissionservices/2016884/297a96656b5846ad8b00d5d41b256ea7"

            payload = "{\r\n    \"Destination\": " + account_number + ",\r\n    \"Amount\": " + amount + ",\r\n    \"CallbackUrl\": \"https://webhook.site/9125cb31-9481-47ad-972f-d1d7765a5957\",\r\n    \"ClientReference\": \"TestEVD01027\"\r\n}"
            headers = {
            'Authorization': config("HUBTEL_API_KEY"),
            'Content-Type': 'text/plain'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            if response.status_code == 200:
                return redirect('thank_you')
            else:
                return redirect("failed")
                    
            form = TVForm()
            return render(request, 'store/layouts/dstv.html', context={'form': form})

            break