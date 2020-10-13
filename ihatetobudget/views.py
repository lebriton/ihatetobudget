from django.shortcuts import redirect, render


def index(request):
    return (
        redirect("sheets:index")
        if request.user.is_authenticated
        else render(
            request, "ihatetobudget/index.html", context={"title": "Home"}
        )
    )
