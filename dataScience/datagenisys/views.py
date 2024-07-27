import pandas as pd
from django.shortcuts import render, redirect
from django.http import HttpResponse


def home_page(request):
    return render(request,'datagenisys/home_page.html')

def about_us(request):
     return render(request,'datagenisys/about_us.html')

def get_dataset(request):
    if request.method == 'POST':
        csv_file = request.FILES['csvFile']
        target_variable = request.POST['targetVariable']
        dataframe = pd.read_csv(csv_file)
        return redirect('about_us_page')
    return HttpResponse("fail")