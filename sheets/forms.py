from django.forms import ModelForm

from .models import Expense


class ExpenseForm(ModelForm):
    class Meta:
        model = Expense
        fields = "__all__"
