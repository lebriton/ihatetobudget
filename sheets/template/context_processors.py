from ..models import Expense


def month_list(request):
    #  XXX: `request.user.is_authenticated` should be enough, since all expenses
    # are available to any user.
    return (
        {"month_list": Expense.objects.dates("date", "month")}
        if request.user.is_authenticated
        else {}
    )
