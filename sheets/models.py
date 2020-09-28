from datetime import date

from colorfield.fields import ColorField
from django.db import models
from django.urls import reverse


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
    amount = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse(
            "sheets:sheet",
            kwargs={"year": self.date.year, "month": self.date.month},
        )
