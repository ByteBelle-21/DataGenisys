from django.shortcuts import render

def home_page(request):
    return render(request,'datagenisys/home_page.html')
