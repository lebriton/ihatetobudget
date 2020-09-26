from django.urls import path

from . import views

app_name = "sheets"
urlpatterns = [
    path("", views.index, name="index"),
    path(
        "<int:year>/<int:month>/",
        views.SheetView.as_view(month_format="%m"),
        name="sheet",
    ),
    path("expense/new/", views.ExpenseCreateView.as_view(), name="expense-new"),
    path(
        "expense/<int:pk>/",
        views.ExpenseUpdateView.as_view(),
        name="expense-edit",
    ),
]
