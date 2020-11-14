import datetime

from ..models import Expense


def month_list(request):
    #  XXX: `request.user.is_authenticated` should be enough, since all expenses
    # are available to any user.
    return (
        {"month_list": Expense.objects.dates("date", "month")}
        if request.user.is_authenticated
        else {}
    )


def current_sheet_dict(request):
    now = datetime.datetime.now()
    for m in month_list(request).get("month_list", []):
        if now.month == m.month and now.year == m.year:
            return {"current_sheet_dict": m}
    return {}
