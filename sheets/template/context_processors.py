import datetime

from ..models import Expense


def sheet_date_list(request):
    #  XXX: `request.user.is_authenticated` should be enough, since all expenses
    # are available to any user.
    return (
        {"sheet_date_list": Expense.objects.dates("date", "month")}
        if request.user.is_authenticated
        else {}
    )


def current_sheet_date(request):
    today = datetime.datetime.today()
    for sheet_date in sheet_date_list(request).get("sheet_date_list", []):
        if sheet_date.month == today.month and sheet_date.year == today.year:
            return {"current_sheet_date": sheet_date}
    return {}
