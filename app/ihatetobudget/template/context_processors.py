from ihatetobudget import __version__


def version(request):
    return {"version": __version__}
