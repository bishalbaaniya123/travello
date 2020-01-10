from django.shortcuts import render, redirect


def test(request):
    print("hello world")
    return render(request, 'index.html')
