from django.forms import ModelForm

from .models import Category, Expense


class ExpenseForm(ModelForm):
    required_css_class = "form-group-required"

    class Meta:
        model = Expense
        fields = "__all__"


class CategoryForm(ModelForm):
    required_css_class = "form-group-required"

    class Meta:
        model = Category
        fields = "__all__"
