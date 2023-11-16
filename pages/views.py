from django.shortcuts import render


def tariffs_page_view(request):
    return render(request, "tariffs_page.html")


def tariff_page_view(request):
    return render(request, "tariff_page.html")


def success_page_view(request):
    return render(request, "success_page.html")
