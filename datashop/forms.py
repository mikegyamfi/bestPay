from django import forms

class AirtimeForm(forms.Form):
    phone = forms.IntegerField(label='Phone Number', required=True, help_text="Number must start with 233 and exclude 0 after 233. Eg. 2332XXXXXXXX")
    # provider = forms.ChoiceField(label='Provider', choices=[(1, 'MTN'), (2, 'AirtelTigo'), (3, 'Vodafone')], required=True)
    amount = forms.FloatField(label='Amount', required=True)

    def clean(self):
        cleaned_data = super(AirtimeForm, self).clean()
        phone = cleaned_data.get('phone')
        amount = cleaned_data.get('amount')
        if not phone and not amount and not provider:
            raise forms.ValidationError('Fill all the spaces provided!')
        if phone:
            if str(phone)[:3] != "233":
                raise forms.ValidationError('Number must start with country code: Eg. 233XXXXXXXXX')
            if len(str(phone)) != 12:
                raise forms.ValidationError('Check your number and try again. You may want to exclude the "0" after 233')



class BundleForm(forms.Form):
    phone = forms.IntegerField(label='Phone Number', required=True, help_text="Number must start with 233 and exclude 0 after 233. Eg. 2332XXXXXXXX")

    def clean(self):
        cleaned_data = super(BundleForm, self).clean()
        phone = cleaned_data.get('phone')
        if not phone:
            raise forms.ValidationError('Fill all the spaces provided!')
        if phone:
            if str(phone)[:3] != "233":
                raise forms.ValidationError('Number must start with country code: Eg. 233XXXXXXXXX')
            if len(str(phone)) != 12:
                raise forms.ValidationError('Check your number and try again. You may want to exclude the "0" after 233')
