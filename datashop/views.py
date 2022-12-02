from django.shortcuts import render
import requests
from .forms import AirtimeForm
from django.contrib import messages

# Create your views here.
def home(request):
    if request.method == 'POST':
        form = AirtimeForm(request.POST)
        if form.is_valid():
            phone_number = str(form.cleaned_data['phone'])
            amount = str(form.cleaned_data['amount'])
            provider = str(form.cleaned_data['provider'])
            url = ""

            mtn_url = "https://cs.hubtel.com/commissionservices/2016884/fdd76c884e614b1c8f669a3207b09a98"
            airtel_tigo_url = "https://cs.hubtel.com/commissionservices/2016884/dae2142eb5a14c298eace60240c09e4b"
            voda_url = "https://cs.hubtel.com/commissionservices/2016884/f4be83ad74c742e185224fdae1304800"

            payload = "{\r\n    \"Destination\": " + phone_number + ",\r\n    \"Amount\": " + amount + ",\r\n    \"CallbackUrl\": \"https://webhook.site/fcad8efa-624b-44c8-a129-b1c01921191d\",\r\n    \"ClientReference\": \"TestEVD01027\"\r\n}"
            
            headers = {
            'Authorization': 'Basic VnY3MHhuTTplNTAzYzcyMGYzYzA0N2Q2ODNjYTM3MWQ5YWEwMDZkZg==',
            'Content-Type': 'text/plain'
            }

            if provider == '1' and phone_number[4] == '4' or phone_number[4] == '9':
                url = mtn_url
            elif provider == '2' and phone_number[4] == '7':
                url = airtel_tigo_url
            elif provider == '3' and phone_number[4] == '0':
                url = voda_url
            else:
                messages.info(request, "Check your provider")
                return render(request, 'store/layouts/index.html', context={'form': form}) 
            # if provider == '1' and phone_number[4] != '4' or phone_number[4] != '9':
            #     messages.info(request, "Check your provider")
            #     return render(request, 'store/layouts/index.html', context={'form': form})
            # if provider == '2' and phone_number[4] != '7':
            #     messages.info(request, "Check your provider")
            #     return render(request, 'store/layouts/index.html', context={'form': form})
            # if provider == '3' and phone_number[4] != '0':
            #     messages.info(request, "Check your provider")
            #     return render(request, 'store/layouts/index.html', context={'form': form})

            response = requests.request("POST", url, headers=headers, data=payload)

            data = response.json()
            print(data)
            

            return render(request, 'store/layouts/index.html', context={'form': form})
    else:
        form = AirtimeForm()
    return render(request, 'store/layouts/index.html', context={'form': form})