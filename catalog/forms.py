from django import forms
import datetime
from .models import Book
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _



class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (Default is 3)")

    # validate the renewal_date

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        # check if date entered is in the past
        if data < datetime.date.today():
            raise VaidationError(_('Invalid date - renewal date is in past'))

        # check if entered date is greater than 4 weeks
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Inavlid date - renewal date is more than 4 weeks'))

        # return the cleaned data
        return data
