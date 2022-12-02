from django.shortcuts import render
import requests
from .forms import AirtimeForm
from django.contrib import messages

# Create your views here.
def mtn_request(request):
    if request.method == 'POST':
        form = AirtimeForm(request.POST)
        if form.is_valid():
            phone_number = str(form.cleaned_data['phone'])
            amount = str(form.cleaned_data['amount'])

            mtn_url = "https://cs.hubtel.com/commissionservices/2016884/fdd76c884e614b1c8f669a3207b09a98"

            payload = "{\r\n    \"Destination\": " + phone_number + ",\r\n    \"Amount\": " + amount + ",\r\n    \"CallbackUrl\": \"https://webhook.site/fcad8efa-624b-44c8-a129-b1c01921191d\",\r\n    \"ClientReference\": \"TestEVD01027\"\r\n}"
            
            headers = {
            'Authorization': 'Basic VnY3MHhuTTplNTAzYzcyMGYzYzA0N2Q2ODNjYTM3MWQ5YWEwMDZkZg==',
            'Content-Type': 'text/plain'
            }

            response = requests.request("POST", mtn_url, headers=headers, data=payload)

            if response.status_code == 200:
                messages.info(request, "Successful")
            else:
                messages.info(request, "Try again Later")
            

            return render(request, 'store/layouts/mtn.html', context={'form': form})
    else:
        form = AirtimeForm()
    return render(request, 'store/layouts/mtn.html', context={'form': form})


def voda_request(request):
    if request.method == 'POST':
        form = AirtimeForm(request.POST)
        if form.is_valid():
            phone_number = str(form.cleaned_data['phone'])
            amount = str(form.cleaned_data['amount'])

            voda_url = "https://cs.hubtel.com/commissionservices/2016884/f4be83ad74c742e185224fdae1304800"

            payload = "{\r\n    \"Destination\": " + phone_number + ",\r\n    \"Amount\": " + amount + ",\r\n    \"CallbackUrl\": \"https://webhook.site/fcad8efa-624b-44c8-a129-b1c01921191d\",\r\n    \"ClientReference\": \"TestEVD01027\"\r\n}"
            
            headers = {
            'Authorization': 'Basic VnY3MHhuTTplNTAzYzcyMGYzYzA0N2Q2ODNjYTM3MWQ5YWEwMDZkZg==',
            'Content-Type': 'text/plain'
            }

            response = requests.request("POST", voda_url, headers=headers, data=payload)

            if response.status_code == 200:
                messages.info(request, "Successful")
            

            return render(request, 'store/layouts/voda.html', context={'form': form})
    else:
        form = AirtimeForm()
    return render(request, 'store/layouts/voda.html', context={'form': form})


def airtel_tigo_request(request):
    if request.method == 'POST':
        form = AirtimeForm(request.POST)
        if form.is_valid():
            phone_number = str(form.cleaned_data['phone'])
            amount = str(form.cleaned_data['amount'])

            airtel_tigo_url = "https://cs.hubtel.com/commissionservices/2016884/dae2142eb5a14c298eace60240c09e4b"

            payload = "{\r\n    \"Destination\": " + phone_number + ",\r\n    \"Amount\": " + amount + ",\r\n    \"CallbackUrl\": \"https://webhook.site/fcad8efa-624b-44c8-a129-b1c01921191d\",\r\n    \"ClientReference\": \"TestEVD01027\"\r\n}"
            
            headers = {
            'Authorization': 'Basic VnY3MHhuTTplNTAzYzcyMGYzYzA0N2Q2ODNjYTM3MWQ5YWEwMDZkZg==',
            'Content-Type': 'text/plain'
            }

            response = requests.request("POST", airtel_tigo_url, headers=headers, data=payload)

            if response.status_code == 200:
                messages.info(request, "Successful")
            

            return render(request, 'store/layouts/tigo.html', context={'form': form})
    else:
        form = AirtimeForm()
    return render(request, 'store/layouts/tigo.html', context={'form': form})