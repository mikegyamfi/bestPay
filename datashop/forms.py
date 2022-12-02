from django import forms

class AirtimeForm(forms.Form):
    phone = forms.IntegerField(label='Phone Number', required=True)
    # provider = forms.ChoiceField(label='Provider', choices=[(1, 'MTN'), (2, 'AirtelTigo'), (3, 'Vodafone')], required=True)
    amount = forms.FloatField(label='Amount', required=True)

    def clean(self):
        cleaned_data = super(AirtimeForm, self).clean()
        phone = cleaned_data.get('phone')
        amount = cleaned_data.get('amount')
        provider = cleaned_data.get('provider')
        if not phone and not amount and not provider:
            raise forms.ValidationError('Fill all the spaces provided!')