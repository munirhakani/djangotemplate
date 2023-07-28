from django import forms
from application.models import Order


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ('notes', )
        widgets = {
            'notes': forms.Textarea(attrs={'placeholder': 'Notes', 'style': 'height: 100px;'}),
        }