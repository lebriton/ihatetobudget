from django.forms import ModelForm

from .models import Expense


class ExpenseForm(ModelForm):
    required_css_class = "form-group-required"

    class Meta:
        model = Expense
        fields = "__all__"
