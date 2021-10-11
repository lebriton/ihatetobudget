from datetime import date
from decimal import Decimal

from colorfield.fields import ColorField
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class Category(models.Model):
    name = models.CharField(max_length=200)
    color = ColorField(default="#FFFFFF")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            "sheets:categories",
        )


class Expense(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )

    date = models.DateField(default=date.today)
    description = models.CharField(max_length=200)
    amount = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    repeat_next_month = models.BooleanField(
        default=False,
        verbose_name=_("Repeat next month?"),
        help_text=_(
            "If checked, this expense will be automatically duplicated at the"
            " start of next month. This is particularly useful for monthly"
            " subscriptions."
        ),
    )
    image = models.ImageField(upload_to="expenses", blank=True, null=True)

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse(
            "sheets:sheet",
            kwargs={"year": self.date.year, "month": self.date.month},
        )
