import datetime

from dateutil import relativedelta

from sheets.models import Expense


def recurring_expenses():

    today = datetime.datetime.today()
    last_day_of_previous_month = today.replace(day=1) - datetime.timedelta(
        days=1
    )

    for expense in Expense.objects.filter(
        repeat_next_month=True,
        date__year=last_day_of_previous_month.year,
        date__month=last_day_of_previous_month.month,
    ):
        # Trick to clone the object
        expense.pk = None
        expense.date = expense.date + relativedelta.relativedelta(months=1)
        expense.save()
