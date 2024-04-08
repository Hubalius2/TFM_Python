from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def say_hello(request):
    return HttpResponse('Hello, Django!')

def welcome(request):
    return render(request, 'welcome.html')

def carApp(request):
    return render(request, 'carApp.html')

def oil_car(request):
    return render(request, 'oil_car.html')