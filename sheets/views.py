from collections import defaultdict

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Sum
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.dates import MonthArchiveView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from ihatetobudget.utils.views import InitialDataAsGETOptionsMixin

from .forms import CategoryForm, ExpenseForm
from .models import Category, Expense


@login_required
def index(request):
    #  XXX: this whole section can probably be optimized/rewritten.
    # <>
    monthly_insights = defaultdict(lambda: defaultdict(list))

    categories = Category.objects.all()
    years = [d.year for d in Expense.objects.dates("date", "year")]
    for year in range(years[0], years[-1] + 1):
        if year not in years:
            continue

        for month in range(1, 13):
            for category in [None] + list(categories):
                monthly_insights[year][category].append(
                    Expense.objects.filter(
                        date__year=year, date__month=month, category=category
                    ).aggregate(Sum("amount"))["amount__sum"]
                    or 0
                )

    #  XXX: Django templates don't work well with defaultdicts
    monthly_insights.default_factory = None
    for category_dict in monthly_insights.values():
        category_dict.default_factory = None
    # </>

    return render(
        request, "sheets/index.html", dict(monthly_insights=monthly_insights)
    )


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
    template_name = "ihatetobudget/generic/new-edit-form.html"
    form_class = ExpenseForm
    extra_context = {"title": "New Expense"}

    # InitialDataAsGETOptionsMixin
    fields_with_initial_data_as_get_option = [
        (
            "category",
            lambda option_value: Category.objects.get(name=option_value),
        )
    ]

    # SuccessMessageMixin
    success_message = "Expense added!"


class ExpenseUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = "ihatetobudget/generic/new-edit-form.html"
    model = Expense
    form_class = ExpenseForm
    extra_context = {"title": "Edit Expense"}

    # SuccessMessageMixin
    success_message = "Expense modified!"


class ExpenseDeleteView(LoginRequiredMixin, DeleteView):
    #  XXX: a `template_name` must be defined if we want to delete via GET.
    #  Currently, we delete via POST (no need to render a template, since we
    #  redirect).

    model = Expense
    success_url = reverse_lazy("sheets:index")

    # SuccessMessageMixin
    success_message = "Expense deleted!"

    def delete(self, request, *args, **kwargs):
        #  XXX: SuccessMessageMixin not working with DeleteView
        messages.success(self.request, self.success_message)

        super_redirect = super().delete(request, *args, **kwargs)
        object = self.object
        if self.model.objects.filter(
            date__year=object.date.year, date__month=object.date.month
        ).first():
            #  There's a least one other object with the same year and month
            return redirect(object.get_absolute_url())
        return super_redirect


class ExpenseListView(LoginRequiredMixin, ListView):
    template_name = "sheets/history.html"
    paginate_by = 10
    model = Expense
    ordering = ["-date"]


class CategoryListView(LoginRequiredMixin, ListView):
    template_name = "sheets/categories.html"
    model = Category


class CategoryCreateView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    CreateView,
):
    template_name = "ihatetobudget/generic/new-edit-form.html"
    form_class = CategoryForm
    extra_context = {"title": "New Category"}

    # SuccessMessageMixin
    success_message = "Category added!"


class CategoryUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = "ihatetobudget/generic/new-edit-form.html"
    model = Category
    form_class = CategoryForm
    extra_context = {"title": "Edit Category"}

    # SuccessMessageMixin
    success_message = "Category modified!"


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "ihatetobudget/generic/delete-form.html"
    model = Category
    extra_context = {"title": "Delete Category"}
    success_url = reverse_lazy("sheets:categories")

    # SuccessMessageMixin
    success_message = "Category deleted!"

    def delete(self, request, *args, **kwargs):
        #  XXX: SuccessMessageMixin not working with DeleteView
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)
