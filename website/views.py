from django.shortcuts import redirect


def home_page(request):
    return redirect('/smallsite/')
