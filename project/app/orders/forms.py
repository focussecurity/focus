# -*- coding: utf-8 -*-
from django.forms import ModelForm
from core.widgets import *
from core.shortcuts import get_company_users
from models import *

class OrderForm(ModelForm):
    #delivery_date = forms.DateField(required=True, input_formats=["%d.%m.%Y"],
    #                                widget=DatePickerField(format="%d.%m.%Y"))
    #delivery_date_deadline = forms.DateField(required=True, input_formats=["%d.%m.%Y"],
    #                                         widget=DatePickerField(format="%d.%m.%Y"))

    class Meta:
        model = Order
        fields = ("oid","POnumber","order_name","customer","project","responsible")
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
      
        if 'instance' in kwargs:
            self.id = kwargs['instance'].id

    def clean_delivery_date_deadline(self):
        delivery_date = self.cleaned_data['delivery_date']
        delivery_date_deadline = self.cleaned_data['delivery_date_deadline']

        if delivery_date_deadline < delivery_date:
            raise forms.ValidationError(u"Tidsfristen må være etter leveringsdato")

        return delivery_date

    def clean_oid(self):
        oid = self.cleaned_data['oid']

        orders = Order.objects.all()
        for i in orders:
            if self.id == i.id:
                continue

            if i.oid == oid:
                raise forms.ValidationError("Det kreves unikt ordrenr")

        return oid

class OrderFormSimple(ModelForm):
    class Meta:
        model = Order
        exclude = ('deleted', 'trashed','date_created', 'date_edited', 'owner', 'creator', 'editor', 'company', 'contacts',
                   'participant',)

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ('text',)