from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.dates import MonthArchiveView
from django.views.generic.edit import FormView

from ihatetobudget.utils.views import InitialDataAsGETOptionsMixin

from .forms import ExpenseForm
from .models import Category, Expense


@login_required
def index(request):
    return render(request, "sheets/index.html")


class ExpenseMonthArchiveView(LoginRequiredMixin, MonthArchiveView):
    template_name = "sheets/sheet.html"
    queryset = Expense.objects.all()
    date_field = "date"
    allow_future = True


class ExpenseFormView(
    LoginRequiredMixin, InitialDataAsGETOptionsMixin, FormView
):
    template_name = "sheets/new_expense.html"
    form_class = ExpenseForm
    success_url = reverse_lazy("sheets:index")

    # InitialDataAsGETOptionsMixin
    fields_with_initial_data_as_get_option = [
        (
            "category",
            lambda option_value: Category.objects.get(name=option_value),
        )
    ]

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
