# noinspection PyPackageRequirements
from datetimewidget.widgets import DateTimeWidget
from django import forms

from app.models import Product


class NewProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('product_card', 'amount', 'amount_unit', 'production_date', 'purchase_date')
        dateTimeOptions = {
            'format': 'dd.mm.yyyy hh:ii',
            'autoclose': 'true',
            'weekStart': '1',
            'todayBtn': 'true',
            'todayHighlight': 'true',
        }
        widgets = {
            'production_date': DateTimeWidget(options=dateTimeOptions),
            'purchase_date': DateTimeWidget(options=dateTimeOptions)
        }
