from datetime import date

from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Expense(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, blank=True
    )

    date = models.DateField(default=date.today)
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.date.isoformat()} - {self.amount} - {self.description} ({self.category})"  # noqa: E501

    def get_absolute_url(self):
        return reverse(
            "sheets:sheet",
            kwargs={"year": self.date.year, "month": self.date.month},
        )
