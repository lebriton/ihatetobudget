import calendar
import datetime
import statistics
from collections import defaultdict

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Avg, Q, Sum
from django.db.models.functions import TruncMonth
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.dates import MonthArchiveView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from ihatetobudget.utils.views import (
    InitialDataAsGETOptionsMixin,
    SortableListViewMixin,
    SuccessMessageOnDeleteViewMixin,
)

from .forms import CategoryForm, ExpenseForm
from .models import Category, Expense


@login_required
def index(request):
    # XXX: this whole section can probably be optimized/rewritten.
    # <>
    monthly_insights = defaultdict(lambda: defaultdict(list))

    if years := [e.year for e in Expense.objects.dates("date", "year")]:
        categories = Category.objects.all()
        for year in years:
            for month in range(1, 13):
                for category in [None] + list(categories):
                    monthly_insights[year][category].append(
                        Expense.objects.filter(
                            date__year=year,
                            date__month=month,
                            category=category,
                        ).aggregate(Sum("amount"))["amount__sum"]
                        or 0
                    )

        # Django templates don't work well with defaultdicts
        monthly_insights.default_factory = None
        for category_dict in monthly_insights.values():
            category_dict.default_factory = None
    # </>

    first_day_of_current_month = datetime.datetime.today().replace(day=1)

    return render(
        request,
        "sheets/index.html",
        dict(
            title="Overview",
            monthly_average_spend=(
                x
                if (
                    x := Expense.objects.filter(
                        date__lt=first_day_of_current_month
                    )
                    .annotate(period=TruncMonth("date"))
                    .values("period")
                    .annotate(amount__sum=Sum("amount"))
                    .aggregate(Avg("amount__sum"))["amount__sum__avg"]
                )
                else 0
            ),
            median_spend=(
                statistics.median(e.amount for e in x)
                if (x := Expense.objects.all())
                else 0
            ),
            monthly_insights_dict=monthly_insights,
            # Currency related
            currency_group_separator=settings.CURRENCY_GROUP_SEPARATOR,
            currency_decimal_separator=settings.CURRENCY_DECIMAL_SEPARATOR,
            currency_prefix=settings.CURRENCY_PREFIX,
            currency_suffix=settings.CURRENCY_SUFFIX,
        ),
    )


class SheetView(LoginRequiredMixin, MonthArchiveView):
    template_name = "sheets/sheet.html"
    queryset = Expense.objects.all()
    date_field = "date"
    allow_future = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = datetime.datetime.today()
        month = context["month"]
        if today.month == month.month and today.year == month.year:
            context["days_left"] = (
                calendar.monthrange(year=today.year, month=today.month)[1]
                - today.day
            ) + 1
        return context


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
    fields_with_initial_data_as_get_option = {
        "category": lambda option_value: Category.objects.get(
            name=option_value
        ),
        "date": None,
        "description": None,
        "amount": None,
        "repeat_next_month": lambda option_value: option_value == "True",
    }

    # SuccessMessageMixin
    success_message = "Expense added!"


class ExpenseUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = "ihatetobudget/generic/new-edit-form.html"
    model = Expense
    form_class = ExpenseForm
    extra_context = {"title": "Edit Expense"}

    # SuccessMessageMixin
    success_message = "Expense modified!"


class ExpenseDeleteView(
    LoginRequiredMixin, SuccessMessageOnDeleteViewMixin, DeleteView
):
    #  XXX: a `template_name` must be defined if we want to delete via GET.
    #  Currently, we delete via POST (no need to render a template, since we
    #  redirect).

    model = Expense
    success_url = reverse_lazy("sheets:index")

    # SuccessMessageMixin
    success_message = "Expense deleted!"

    def get_success_url(self):
        object = self.object
        # XXX: this can probably be optimized
        if similar_object := (
            self.model.objects.exclude(pk=object.pk)
            .filter(date__year=object.date.year, date__month=object.date.month)
            .first()
        ):
            #  There's a least one other object with the same year and month
            return similar_object.get_absolute_url()
        return super().get_success_url()


class ExpenseListView(LoginRequiredMixin, SortableListViewMixin, ListView):
    template_name = "sheets/history.html"
    paginate_by = 50
    model = Expense
    ordering = ["-date"]
    extra_context = {"title": "Expense History"}

    # SortableListViewMixin
    sortable_fields = ["date", "category", "amount"]

    def get_queryset(self):
        queryset = super().get_queryset()
        if query := self.request.GET.get("q"):
            return queryset.filter(
                Q(date__icontains=query)
                | Q(category__name__icontains=query)
                | Q(amount__icontains=query)
                | Q(description__icontains=query)
            )
        return queryset


class CategoryListView(LoginRequiredMixin, ListView):
    template_name = "sheets/categories.html"
    model = Category
    extra_context = {"title": "Categories"}


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


class CategoryDeleteView(
    LoginRequiredMixin, SuccessMessageOnDeleteViewMixin, DeleteView
):
    template_name = "ihatetobudget/generic/delete-form.html"
    model = Category
    extra_context = {"title": "Delete Category"}
    success_url = reverse_lazy("sheets:categories")

    # SuccessMessageMixin
    success_message = "Category deleted!"
