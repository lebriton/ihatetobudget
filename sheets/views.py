from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.views.generic.dates import MonthArchiveView
from django.views.generic.edit import CreateView, UpdateView

from ihatetobudget.utils.views import InitialDataAsGETOptionsMixin

from .forms import ExpenseForm
from .models import Category, Expense


@login_required
def index(request):
    return render(request, "sheets/index.html")


class SheetView(LoginRequiredMixin, MonthArchiveView):
    template_name = "sheets/sheet.html"
    queryset = Expense.objects.all()
    date_field = "date"
    allow_future = True


class ExpenseCreateView(
    LoginRequiredMixin,
    InitialDataAsGETOptionsMixin,
    SuccessMessageMixin,
    CreateView,
):
    template_name = "sheets/expense/create-update.html"
    form_class = ExpenseForm

    # InitialDataAsGETOptionsMixin
    fields_with_initial_data_as_get_option = [
        (
            "category",
            lambda option_value: Category.objects.get(name=option_value),
        )
    ]

    # SuccessMessageMixin
    success_message = "Expense successfully created!"


class ExpenseUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = "sheets/expense/create-update.html"
    model = Expense
    form_class = ExpenseForm

    # SuccessMessageMixin
    success_message = "Expense successfully changed!"
