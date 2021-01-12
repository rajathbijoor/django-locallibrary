from django import forms
import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User
from catalog.models import UserProfileInfo

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date between today and the 4th week(default is 3)")

    def clean_renewal_date(self):
        data = self.clean_renewal_date['renewal_date']

        #check if date is not in the past
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'),)

        #check if a date is in the allowed range(+4 weeks from today)
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'), )

        return data

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'email', 'password')

class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('portfolio_site', 'profile_pic')