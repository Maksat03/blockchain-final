from django.shortcuts import redirect
from .services import subscribe


def subscribe_view(request):
    if request.method == "POST":
        subscribe(request.POST)
        return redirect("/success/")
    return redirect("/")
