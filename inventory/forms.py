from django import forms
import datetime


class OrderForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        for i in range(1, 100):
            self.fields['order_' + str(i)] = forms.CharField()


form = OrderForm()
