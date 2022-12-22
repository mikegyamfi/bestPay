from django.shortcuts import render, redirect, reverse
import requests
from ..forms import BundleForm
from django.contrib import messages
import json
from django.http import HttpResponse
import random
from decouple import config

def pay_for_v1_bundle(request):
    client_ref = 'gds'+str(random.randint(11111111, 99999999))

    if request.method == "POST":
        form = BundleForm(request.POST)
        if form.is_valid():
            phone_number = str(form.cleaned_data["phone"])
            amount = 0.90   

            url = "https://payproxyapi.hubtel.com/items/initiate"

            payload = json.dumps({
            "totalAmount": amount,
            "description": "Video 183.49MB",
            "callbackUrl": 'https://webhook.site/d53f5c53-eaba-4139-ad27-fb05b0a7be7f',
            "returnUrl": f'https://bestpay-app-id6nm.ondigitalocean.app/send_v1_mtn_bundle/{client_ref}/{phone_number}',
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
    else:
        form = BundleForm(initial={'phone':233})
    return render(request, "store/layouts/mtn_bundle.html", {'form': form})


def send_v1_bundle(request, client_ref, phone_number):
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
                return redirect(f"https://bestpay-app-id6nm.ondigitalocean.app/send_v1_mtn_bundle/{client_ref}/{phone_number}")
            status = content["Status"]
            ref = content["Data"]["ClientReference"]
        except KeyError:
            return redirect("failed")
        if ref == client_ref and status == "Success":
            url = "https://cs.hubtel.com/commissionservices/2016884/b230733cd56b4a0fad820e39f66bc27c"

            payload = "{\r\n    \"Destination\": " + phone_number + ",\r\n    \"Amount\": 1.0,\r\n    \"CallbackUrl\": \"https://webhook.site/9125cb31-9481-47ad-972f-d1d7765a5957\",\r\n    \"ClientReference\": \"GHDS10001\",\r\n    \"Extradata\" : {\r\n        \"bundle\" : \"video_bundle_1\"\r\n    }\r\n}\r\n"
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

######################################### 5 CEDI Video ######################################################

def pay_for_v5_bundle(request):
    client_ref = 'gds'+str(random.randint(11111111, 99999999))

    if request.method == "POST":
        form = BundleForm(request.POST)
        if form.is_valid():
            phone_number = str(form.cleaned_data["phone"])
            amount = 4.90 

            url = "https://payproxyapi.hubtel.com/items/initiate"

            payload = json.dumps({
            "totalAmount": amount,
            "description": "Video 917.43MB",
            "callbackUrl": 'https://webhook.site/d53f5c53-eaba-4139-ad27-fb05b0a7be7f',
            "returnUrl": f'https://bestpay-app-id6nm.ondigitalocean.app/send_v5_mtn_bundle/{client_ref}/{phone_number}',
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
    else:
        form = BundleForm(initial={'phone':233})
    return render(request, "store/layouts/mtn_bundle.html", {'form': form})


def send_v5_bundle(request, client_ref, phone_number):
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
                return redirect(f"https://bestpay-app-id6nm.ondigitalocean.app/send_v5_mtn_bundle/{client_ref}/{phone_number}")
            status = content["Status"]
            ref = content["Data"]["ClientReference"]
        except KeyError:
            return redirect("failed")
        if ref == client_ref and status == "Success":
            url = "https://cs.hubtel.com/commissionservices/2016884/b230733cd56b4a0fad820e39f66bc27c"

            payload = "{\r\n    \"Destination\": " + phone_number + ",\r\n    \"Amount\": 5.0,\r\n    \"CallbackUrl\": \"https://webhook.site/9125cb31-9481-47ad-972f-d1d7765a5957\",\r\n    \"ClientReference\": \"GHDS10001\",\r\n    \"Extradata\" : {\r\n        \"bundle\" : \"video_bundle_2\"\r\n    }\r\n}\r\n"
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

######################################### 10 CEDI VIDEO ######################################################

def pay_for_v10_bundle(request):
    client_ref = 'gds'+str(random.randint(11111111, 99999999))

    if request.method == "POST":
        form = BundleForm(request.POST)
        if form.is_valid():
            phone_number = str(form.cleaned_data["phone"])
            amount = 9.90

            url = "https://payproxyapi.hubtel.com/items/initiate"

            payload = json.dumps({
            "totalAmount": amount,
            "description": "Video 1.79GB",
            "callbackUrl": 'https://webhook.site/d53f5c53-eaba-4139-ad27-fb05b0a7be7f',
            "returnUrl": f'https://bestpay-app-id6nm.ondigitalocean.app/send_v10_mtn_bundle/{client_ref}/{phone_number}',
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
    else:
        form = BundleForm(initial={'phone':233})
    return render(request, "store/layouts/mtn_bundle.html", {'form': form})


def send_v10_bundle(request, client_ref, phone_number):
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
                return redirect(f"https://bestpay-app-id6nm.ondigitalocean.app/send_v10_mtn_bundle/{client_ref}/{phone_number}")
            status = content["Status"]
            ref = content["Data"]["ClientReference"]
        except KeyError:
            return redirect("failed")
        if ref == client_ref and status == "Success":
            url = "https://cs.hubtel.com/commissionservices/2016884/b230733cd56b4a0fad820e39f66bc27c"

            payload = "{\r\n    \"Destination\": " + phone_number + ",\r\n    \"Amount\": 10.0,\r\n    \"CallbackUrl\": \"https://webhook.site/9125cb31-9481-47ad-972f-d1d7765a5957\",\r\n    \"ClientReference\": \"GHDS10001\",\r\n    \"Extradata\" : {\r\n        \"bundle\" : \"video_bundle_3\"\r\n    }\r\n}\r\n"
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

######################################### 1 CEDI SOCIAL ######################################################

def pay_for_s1_bundle(request):
    client_ref = 'gds'+str(random.randint(11111111, 99999999))

    if request.method == "POST":
        form = BundleForm(request.POST)
        if form.is_valid():
            phone_number = str(form.cleaned_data["phone"])
            amount = 0.90

            url = "https://payproxyapi.hubtel.com/items/initiate"

            payload = json.dumps({
            "totalAmount": amount,
            "description": "Social Media 96.15MB",
            "callbackUrl": 'https://webhook.site/d53f5c53-eaba-4139-ad27-fb05b0a7be7f',
            "returnUrl": f'https://bestpay-app-id6nm.ondigitalocean.app/send_s1_mtn_bundle/{client_ref}/{phone_number}',
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
    else:
        form = BundleForm(initial={'phone':233})
    return render(request, "store/layouts/mtn_bundle.html", {'form': form})


def send_s1_bundle(request, client_ref, phone_number):
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
                return redirect(f"https://bestpay-app-id6nm.ondigitalocean.app/send_s1_mtn_bundle/{client_ref}/{phone_number}")
            status = content["Status"]
            ref = content["Data"]["ClientReference"]
        except KeyError:
            return redirect("failed")
        if ref == client_ref and status == "Success":
            url = "https://cs.hubtel.com/commissionservices/2016884/b230733cd56b4a0fad820e39f66bc27c"

            payload = "{\r\n    \"Destination\": " + phone_number + ",\r\n    \"Amount\": 1.0,\r\n    \"CallbackUrl\": \"https://webhook.site/9125cb31-9481-47ad-972f-d1d7765a5957\",\r\n    \"ClientReference\": \"GHDS10001\",\r\n    \"Extradata\" : {\r\n        \"bundle\" : \"social_media_bundle_1\"\r\n    }\r\n}\r\n"
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

######################################### 5 CEDI SOCIAL ######################################################

def pay_for_s5_bundle(request):
    client_ref = 'gds'+str(random.randint(11111111, 99999999))

    if request.method == "POST":
        form = BundleForm(request.POST)
        if form.is_valid():
            phone_number = str(form.cleaned_data["phone"])
            amount = 4.90

            url = "https://payproxyapi.hubtel.com/items/initiate"

            payload = json.dumps({
            "totalAmount": amount,
            "description": "Social Media 480.77MB",
            "callbackUrl": 'https://webhook.site/d53f5c53-eaba-4139-ad27-fb05b0a7be7f',
            "returnUrl": f'https://bestpay-app-id6nm.ondigitalocean.app/send_s5_mtn_bundle/{client_ref}/{phone_number}',
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
    else:
        form = BundleForm(initial={'phone':233})
    return render(request, "store/layouts/mtn_bundle.html", {'form': form})


def send_s5_bundle(request, client_ref, phone_number):
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
                return redirect(f"https://bestpay-app-id6nm.ondigitalocean.app/send_s5_mtn_bundle/{client_ref}/{phone_number}")
            status = content["Status"]
            ref = content["Data"]["ClientReference"]
        except KeyError:
            return redirect("failed")
        if ref == client_ref and status == "Success":
            url = "https://cs.hubtel.com/commissionservices/2016884/b230733cd56b4a0fad820e39f66bc27c"

            payload = "{\r\n    \"Destination\": " + phone_number + ",\r\n    \"Amount\": 5.0,\r\n    \"CallbackUrl\": \"https://webhook.site/9125cb31-9481-47ad-972f-d1d7765a5957\",\r\n    \"ClientReference\": \"GHDS10001\",\r\n    \"Extradata\" : {\r\n        \"bundle\" : \"social_media_bundle_2\"\r\n    }\r\n}\r\n"
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

######################################### 10 CEDI SOCIAL ######################################################

def pay_for_s10_bundle(request):
    client_ref = 'gds'+str(random.randint(11111111, 99999999))

    if request.method == "POST":
        form = BundleForm(request.POST)
        if form.is_valid():
            phone_number = str(form.cleaned_data["phone"])
            amount = 9.90

            url = "https://payproxyapi.hubtel.com/items/initiate"

            payload = json.dumps({
            "totalAmount": amount,
            "description": "Social Media 961.54MB",
            "callbackUrl": 'https://webhook.site/d53f5c53-eaba-4139-ad27-fb05b0a7be7f',
            "returnUrl": f'https://bestpay-app-id6nm.ondigitalocean.app/send_s10_mtn_bundle/{client_ref}/{phone_number}',
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
    else:
        form = BundleForm(initial={'phone':233})
    return render(request, "store/layouts/mtn_bundle.html", {'form': form})


def send_s10_bundle(request, client_ref, phone_number):
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
                return redirect(f"https://bestpay-app-id6nm.ondigitalocean.app/send_s10_mtn_bundle/{client_ref}/{phone_number}")
            status = content["Status"]
            ref = content["Data"]["ClientReference"]
        except KeyError:
            return redirect("failed")
        if ref == client_ref and status == "Success":
            url = "https://cs.hubtel.com/commissionservices/2016884/b230733cd56b4a0fad820e39f66bc27c"

            payload = "{\r\n    \"Destination\": " + phone_number + ",\r\n    \"Amount\": 10.0,\r\n    \"CallbackUrl\": \"https://webhook.site/9125cb31-9481-47ad-972f-d1d7765a5957\",\r\n    \"ClientReference\": \"GHDS10001\",\r\n    \"Extradata\" : {\r\n        \"bundle\" : \"social_media_bundle_3\"\r\n    }\r\n}\r\n"
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

######################################### 1 CEDI BUNDLE ######################################################

