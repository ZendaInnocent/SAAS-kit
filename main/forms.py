from django import forms
from django.forms import fields

from .models import Transaction


class TransactionForm(forms.ModelForm):

    class Meta:
        model = Transaction
        fields = ('phone', )
