from django.urls import path

from . import views

app_name = "sheets"
urlpatterns = [
    path("", views.index, name="index"),
    path(
        "<int:year>/<int:month>/",
        views.ExpenseMonthArchiveView.as_view(month_format="%m"),
        name="sheet",
    ),
    path("expenses/new", views.ExpenseFormView.as_view(), name="new_expense"),
]
