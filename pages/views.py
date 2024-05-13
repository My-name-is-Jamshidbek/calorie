from django.shortcuts import render, redirect


def welcome(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        return render(request, 'welcome.html')


def home(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')
    else:
        return render(request, 'welcome.html')

