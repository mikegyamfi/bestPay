from django.shortcuts import render, redirect, reverse
import requests
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
            "returnUrl": f'https://bestpay-app-id6nm.ondigitalocean.app/send_50p_voda_bundle/{client_ref}/{phone_number}',
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
            return render(request, 'store/layouts/voda_bundle.html', context={'form': form})
    else:
        form = BundleForm(initial={'phone':233})
    return render(request, "store/layouts/voda_bundle.html", {'form': form})


def send_50p_bundle(request, client_ref, phone_number):
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
                return redirect(f"https://bestpay-app-id6nm.ondigitalocean.app/send_50p_voda_bundle/{client_ref}/{phone_number}")
            status = content["Status"]
            ref = content["Data"]["ClientReference"]
        except KeyError:
            return redirect("failed")
        if ref == client_ref and status == "Success":
            url = "https://cs.hubtel.com/commissionservices/2016884/fa27127ba039455da04a2ac8a1613e00"

            payload = "{\r\n    \"Destination\": " + phone_number + ",\r\n    \"Amount\": 0.5,\r\n    \"CallbackUrl\": \"https://webhook.site/fcad8efa-624b-44c8-a129-b1c01921191d\",\r\n    \"ClientReference\": \"GHDS10001\",\r\n    \"Extradata\" : {\r\n        \"bundle\" : \"DATANVSTRDLY\"\r\n    }\r\n}\r\n"
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
            return render(request, 'store/layouts/voda_bundle.html', context={'form': form})

            break

########################################### 1 cedi bundle #############################################################3

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
            "description": "65MB Bundle",
            "callbackUrl": 'https://webhook.site/d53f5c53-eaba-4139-ad27-fb05b0a7be7f',
            "returnUrl": f'https://bestpay-app-id6nm.ondigitalocean.app/send_1_voda_bundle/{client_ref}/{phone_number}',
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
            return render(request, 'store/layouts/voda_bundle.html', context={'form': form})
    else:
        form = BundleForm(initial={'phone':233})
    return render(request, "store/layouts/voda_bundle.html", {'form': form})


def send_1_bundle(request, client_ref, phone_number):
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
                return redirect(f"https://bestpay-app-id6nm.ondigitalocean.app/send_1_voda_bundle/{client_ref}/{phone_number}")
            status = content["Status"]
            ref = content["Data"]["ClientReference"]
        except KeyError:
            return redirect("failed")
        if ref == client_ref and status == "Success":
            url = "https://cs.hubtel.com/commissionservices/2016884/fa27127ba039455da04a2ac8a1613e00"

            payload = "{\r\n    \"Destination\": " + phone_number + ",\r\n    \"Amount\": 1,\r\n    \"CallbackUrl\": \"https://webhook.site/fcad8efa-624b-44c8-a129-b1c01921191d\",\r\n    \"ClientReference\": \"GHDS10001\",\r\n    \"Extradata\" : {\r\n        \"bundle\" : \"DATANVDR1DLY\"\r\n    }\r\n}\r\n"
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
            return render(request, 'store/layouts/voda_bundle.html', context={'form': form})

            break

########################################### 2 cedis bundle #############################################################3

def pay_for_2_bundle(request):
    client_ref = 'gds'+str(random.randint(11111111, 99999999))

    if request.method == "POST":
        form = BundleForm(request.POST)
        if form.is_valid():
            phone_number = str(form.cleaned_data["phone"])
            amount = 1.90

            url = "https://payproxyapi.hubtel.com/items/initiate"

            payload = json.dumps({
            "totalAmount": amount,
            "description": "165MB Bundle",
            "callbackUrl": 'https://webhook.site/d53f5c53-eaba-4139-ad27-fb05b0a7be7f',
            "returnUrl": f'https://bestpay-app-id6nm.ondigitalocean.app/send_2_voda_bundle/{client_ref}/{phone_number}',
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
            return render(request, 'store/layouts/voda_bundle.html', context={'form': form})
    else:
        form = BundleForm(initial={'phone':233})
    return render(request, "store/layouts/voda_bundle.html", {'form': form})


def send_2_bundle(request, client_ref, phone_number):
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
                return redirect(f"https://bestpay-app-id6nm.ondigitalocean.app/send_2_voda_bundle/{client_ref}/{phone_number}")
            status = content["Status"]
            ref = content["Data"]["ClientReference"]
        except KeyError:
            return redirect("failed")
        if ref == client_ref and status == "Success":
            url = "https://cs.hubtel.com/commissionservices/2016884/fa27127ba039455da04a2ac8a1613e00"

            payload = "{\r\n    \"Destination\": " + phone_number + ",\r\n    \"Amount\": 2,\r\n    \"CallbackUrl\": \"https://webhook.site/fcad8efa-624b-44c8-a129-b1c01921191d\",\r\n    \"ClientReference\": \"GHDS10001\",\r\n    \"Extradata\" : {\r\n        \"bundle\" : \"DATANVCHTDLY\"\r\n    }\r\n}\r\n"
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
            return render(request, 'store/layouts/voda_bundle.html', context={'form': form})

            break

########################################### 5 cedis bundle #############################################################3

def pay_for_5_bundle(request):
    client_ref = 'gds'+str(random.randint(11111111, 99999999))

    if request.method == "POST":
        form = BundleForm(request.POST)
        if form.is_valid():
            phone_number = str(form.cleaned_data["phone"])
            amount = 4.90

            url = "https://payproxyapi.hubtel.com/items/initiate"

            payload = json.dumps({
            "totalAmount": amount,
            "description": "655MB Bundle",
            "callbackUrl": 'https://webhook.site/d53f5c53-eaba-4139-ad27-fb05b0a7be7f',
            "returnUrl": f'https://bestpay-app-id6nm.ondigitalocean.app/send_5_voda_bundle/{client_ref}/{phone_number}',
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
            return render(request, 'store/layouts/voda_bundle.html', context={'form': form})
    else:
        form = BundleForm(initial={'phone':233})
    return render(request, "store/layouts/voda_bundle.html", {'form': form})


def send_5_bundle(request, client_ref, phone_number):
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
                return redirect(f"https://bestpay-app-id6nm.ondigitalocean.app/send_5_voda_bundle/{client_ref}/{phone_number}")
            status = content["Status"]
            ref = content["Data"]["ClientReference"]
        except KeyError:
            return redirect("failed")
        if ref == client_ref and status == "Success":
            url = "https://cs.hubtel.com/commissionservices/2016884/fa27127ba039455da04a2ac8a1613e00"

            payload = "{\r\n    \"Destination\": " + phone_number + ",\r\n    \"Amount\": 5,\r\n    \"CallbackUrl\": \"https://webhook.site/fcad8efa-624b-44c8-a129-b1c01921191d\",\r\n    \"ClientReference\": \"GHDS10001\",\r\n    \"Extradata\" : {\r\n        \"bundle\" : \"DATANVDR5WLY\"\r\n    }\r\n}\r\n"
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
            return render(request, 'store/layouts/voda_bundle.html', context={'form': form})

            break

########################################### 10 cedis bundle #############################################################3

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
            "description": "1.5GB Bundle",
            "callbackUrl": 'https://webhook.site/d53f5c53-eaba-4139-ad27-fb05b0a7be7f',
            "returnUrl": f'https://bestpay-app-id6nm.ondigitalocean.app/send_10_voda_bundle/{client_ref}/{phone_number}',
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
            return render(request, 'store/layouts/voda_bundle.html', context={'form': form})
    else:
        form = BundleForm(initial={'phone':233})
    return render(request, "store/layouts/voda_bundle.html", {'form': form})


def send_10_bundle(request, client_ref, phone_number):
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
                return redirect(f"https://bestpay-app-id6nm.ondigitalocean.app/send_10_voda_bundle/{client_ref}/{phone_number}")
            status = content["Status"]
            ref = content["Data"]["ClientReference"]
        except KeyError:
            return redirect("failed")
        if ref == client_ref and status == "Success":
            url = "https://cs.hubtel.com/commissionservices/2016884/fa27127ba039455da04a2ac8a1613e00"

            payload = "{\r\n    \"Destination\": " + phone_number + ",\r\n    \"Amount\": 10,\r\n    \"CallbackUrl\": \"https://webhook.site/fcad8efa-624b-44c8-a129-b1c01921191d\",\r\n    \"ClientReference\": \"GHDS10001\",\r\n    \"Extradata\" : {\r\n        \"bundle\" : \"DATANVDBDL1\"\r\n    }\r\n}\r\n"
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
            return render(request, 'store/layouts/voda_bundle.html', context={'form': form})

            break

########################################### 20 cedis bundle #############################################################3

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
            "description": "4GB Bundle",
            "callbackUrl": 'https://webhook.site/d53f5c53-eaba-4139-ad27-fb05b0a7be7f',
            "returnUrl": f'https://bestpay-app-id6nm.ondigitalocean.app/send_20_voda_bundle/{client_ref}/{phone_number}',
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
            return render(request, 'store/layouts/voda_bundle.html', context={'form': form})
    else:
        form = BundleForm(initial={'phone':233})
    return render(request, "store/layouts/voda_bundle.html", {'form': form})


def send_20_bundle(request, client_ref, phone_number):
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
                return redirect(f"https://bestpay-app-id6nm.ondigitalocean.app/send_20_voda_bundle/{client_ref}/{phone_number}")
            status = content["Status"]
            ref = content["Data"]["ClientReference"]
        except KeyError:
            return redirect("failed")
        if ref == client_ref and status == "Success":
            url = "https://cs.hubtel.com/commissionservices/2016884/fa27127ba039455da04a2ac8a1613e00"

            payload = "{\r\n    \"Destination\": " + phone_number + ",\r\n    \"Amount\": 20,\r\n    \"CallbackUrl\": \"https://webhook.site/fcad8efa-624b-44c8-a129-b1c01921191d\",\r\n    \"ClientReference\": \"GHDS10001\",\r\n    \"Extradata\" : {\r\n        \"bundle\" : \"DATANVDBDL2\"\r\n    }\r\n}\r\n"
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
            return render(request, 'store/layouts/voda_bundle.html', context={'form': form})

            break

########################################### 50 cedis bundle #############################################################3

def pay_for_50_bundle(request):
    client_ref = 'gds'+str(random.randint(11111111, 99999999))

    if request.method == "POST":
        form = BundleForm(request.POST)
        if form.is_valid():
            phone_number = str(form.cleaned_data["phone"])
            amount = 49.50

            url = "https://payproxyapi.hubtel.com/items/initiate"

            payload = json.dumps({
            "totalAmount": amount,
            "description": "10.2GB Bundle",
            "callbackUrl": 'https://webhook.site/d53f5c53-eaba-4139-ad27-fb05b0a7be7f',
            "returnUrl": f'https://bestpay-app-id6nm.ondigitalocean.app/send_50_voda_bundle/{client_ref}/{phone_number}',
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
            return render(request, 'store/layouts/voda_bundle.html', context={'form': form})
    else:
        form = BundleForm(initial={'phone':233})
    return render(request, "store/layouts/voda_bundle.html", {'form': form})


def send_50_bundle(request, client_ref, phone_number):
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
                return redirect(f"https://bestpay-app-id6nm.ondigitalocean.app/send_50_voda_bundle/{client_ref}/{phone_number}")
            status = content["Status"]
            ref = content["Data"]["ClientReference"]
        except KeyError:
            return redirect("failed")
        if ref == client_ref and status == "Success":
            url = "https://cs.hubtel.com/commissionservices/2016884/fa27127ba039455da04a2ac8a1613e00"

            payload = "{\r\n    \"Destination\": " + phone_number + ",\r\n    \"Amount\": 50,\r\n    \"CallbackUrl\": \"https://webhook.site/fcad8efa-624b-44c8-a129-b1c01921191d\",\r\n    \"ClientReference\": \"GHDS10001\",\r\n    \"Extradata\" : {\r\n        \"bundle\" : \"DATANVDBDL3\"\r\n    }\r\n}\r\n"
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
            return render(request, 'store/layouts/voda_bundle.html', context={'form': form})

            break

########################################### 100 cedis bundle #############################################################3

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
            "description": "16GB Bundle",
            "callbackUrl": 'https://webhook.site/d53f5c53-eaba-4139-ad27-fb05b0a7be7f',
            "returnUrl": f'https://bestpay-app-id6nm.ondigitalocean.app/send_100_voda_bundle/{client_ref}/{phone_number}',
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
            return render(request, 'store/layouts/voda_bundle.html', context={'form': form})
    else:
        form = BundleForm(initial={'phone':233})
    return render(request, "store/layouts/voda_bundle.html", {'form': form})


def send_100_bundle(request, client_ref, phone_number):
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
                return redirect(f"https://bestpay-app-id6nm.ondigitalocean.app/send_100_voda_bundle/{client_ref}/{phone_number}")
            status = content["Status"]
            ref = content["Data"]["ClientReference"]
        except KeyError:
            return redirect("failed")
        if ref == client_ref and status == "Success":
            url = "https://cs.hubtel.com/commissionservices/2016884/fa27127ba039455da04a2ac8a1613e00"

            payload = "{\r\n    \"Destination\": " + phone_number + ",\r\n    \"Amount\": 100,\r\n    \"CallbackUrl\": \"https://webhook.site/fcad8efa-624b-44c8-a129-b1c01921191d\",\r\n    \"ClientReference\": \"GHDS10001\",\r\n    \"Extradata\" : {\r\n        \"bundle\" : \"DATANVDBDL4\"\r\n    }\r\n}\r\n"
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
            return render(request, 'store/layouts/voda_bundle.html', context={'form': form})

            break

########################################### 200 cedis bundle #############################################################3

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
            "description": "40GB Bundle",
            "callbackUrl": 'https://webhook.site/d53f5c53-eaba-4139-ad27-fb05b0a7be7f',
            "returnUrl": f'https://bestpay-app-id6nm.ondigitalocean.app/send_200_voda_bundle/{client_ref}/{phone_number}',
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
            return render(request, 'store/layouts/voda_bundle.html', context={'form': form})
    else:
        form = BundleForm(initial={'phone':233})
    return render(request, "store/layouts/voda_bundle.html", {'form': form})


def send_200_bundle(request, client_ref, phone_number):
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
                return redirect(f"https://bestpay-app-id6nm.ondigitalocean.app/send_200_voda_bundle/{client_ref}/{phone_number}")
            status = content["Status"]
            ref = content["Data"]["ClientReference"]
        except KeyError:
            return redirect("failed")
        if ref == client_ref and status == "Success":
            url = "https://cs.hubtel.com/commissionservices/2016884/fa27127ba039455da04a2ac8a1613e00"

            payload = "{\r\n    \"Destination\": " + phone_number + ",\r\n    \"Amount\": 200,\r\n    \"CallbackUrl\": \"https://webhook.site/fcad8efa-624b-44c8-a129-b1c01921191d\",\r\n    \"ClientReference\": \"GHDS10001\",\r\n    \"Extradata\" : {\r\n        \"bundle\" : \"DATANVDBDL5\"\r\n    }\r\n}\r\n"
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
            return render(request, 'store/layouts/voda_bundle.html', context={'form': form})

            break

########################################### 300 cedis bundle #############################################################3

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
            "description": "125GB Bundle",
            "callbackUrl": 'https://webhook.site/d53f5c53-eaba-4139-ad27-fb05b0a7be7f',
            "returnUrl": f'https://bestpay-app-id6nm.ondigitalocean.app/send_300_voda_bundle/{client_ref}/{phone_number}',
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
            return render(request, 'store/layouts/voda_bundle.html', context={'form': form})
    else:
        form = BundleForm(initial={'phone':233})
    return render(request, "store/layouts/voda_bundle.html", {'form': form})


def send_300_bundle(request, client_ref, phone_number):
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
                return redirect(f"https://bestpay-app-id6nm.ondigitalocean.app/send_300_voda_bundle/{client_ref}/{phone_number}")
            status = content["Status"]
            ref = content["Data"]["ClientReference"]
        except KeyError:
            return redirect("failed")
        if ref == client_ref and status == "Success":
            url = "https://cs.hubtel.com/commissionservices/2016884/fa27127ba039455da04a2ac8a1613e00"

            payload = "{\r\n    \"Destination\": " + phone_number + ",\r\n    \"Amount\": 300,\r\n    \"CallbackUrl\": \"https://webhook.site/fcad8efa-624b-44c8-a129-b1c01921191d\",\r\n    \"ClientReference\": \"GHDS10001\",\r\n    \"Extradata\" : {\r\n        \"bundle\" : \"DATANVDBDL6\"\r\n    }\r\n}\r\n"
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
            return render(request, 'store/layouts/voda_bundle.html', context={'form': form})

            break

########################################### 400 cedis bundle #############################################################3

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
            "description": "225GB Bundle",
            "callbackUrl": 'https://webhook.site/d53f5c53-eaba-4139-ad27-fb05b0a7be7f',
            "returnUrl": f'https://bestpay-app-id6nm.ondigitalocean.app/send_400_voda_bundle/{client_ref}/{phone_number}',
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
            return render(request, 'store/layouts/voda_bundle.html', context={'form': form})
    else:
        form = BundleForm(initial={'phone':233})
    return render(request, "store/layouts/voda_bundle.html", {'form': form})


def send_400_bundle(request, client_ref, phone_number):
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
                return redirect(f"https://bestpay-app-id6nm.ondigitalocean.app/send_400_voda_bundle/{client_ref}/{phone_number}")
            status = content["Status"]
            ref = content["Data"]["ClientReference"]
        except KeyError:
            return redirect("failed")
        if ref == client_ref and status == "Success":
            url = "https://cs.hubtel.com/commissionservices/2016884/fa27127ba039455da04a2ac8a1613e00"

            payload = "{\r\n    \"Destination\": " + phone_number + ",\r\n    \"Amount\": 400,\r\n    \"CallbackUrl\": \"https://webhook.site/fcad8efa-624b-44c8-a129-b1c01921191d\",\r\n    \"ClientReference\": \"GHDS10001\",\r\n    \"Extradata\" : {\r\n        \"bundle\" : \"DATANVDBDL7\"\r\n    }\r\n}\r\n"
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
            return render(request, 'store/layouts/voda_bundle.html', context={'form': form})

            break

