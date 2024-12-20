from django.forms import ModelForm, TextInput
from .models import History

class CheckoutForm(ModelForm):
    class Meta:
        model = History
        fields = ['name', 'address']

        widgets = {
            'name': TextInput(attrs={'class':'m-2 p-[10px] py-3 rounded-md h-[25px] w-[400px] border-[1px] border-[#00134E] border-opacity-30'}),
            'address': TextInput(attrs={'class':'m-2 p-[10px] py-3 rounded-md h-[25px] w-[400px] border-[1px] border-[#00134E] border-opacity-30'}),
        }