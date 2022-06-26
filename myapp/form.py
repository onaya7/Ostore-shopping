from myapp.models import CustomerInfo
from wtforms import Form

class CustomerInfoForm (Form):
    class Meta:
        model = CustomerInfo
        fields = '__all__'
