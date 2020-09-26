from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.dates import MonthArchiveView
from django.views.generic.edit import FormView

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


class ExpenseFormView(LoginRequiredMixin, FormView):
    template_name = "sheets/new_expense.html"
    form_class = ExpenseForm
    success_url = reverse_lazy("sheets:index")

    def get_initial(self):
        initial = super().get_initial()
        if category := self.request.GET.get("category"):
            try:
                initial["category"] = Category.objects.get(name=category)
            except Category.DoesNotExist:
                pass
        return initial

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
