from django.shortcuts import render, redirect
from django.http import HttpResponse

def index(request):

    return render(request, 'hi.html')

def loginsu(request):

    return render(request, 'loginsu.html')

# Create your views here.
