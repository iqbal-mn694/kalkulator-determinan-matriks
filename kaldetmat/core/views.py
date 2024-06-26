import os
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from dotenv import load_dotenv
from . import functions
import requests

# Create your views here.
load_dotenv()


@require_http_methods(['GET', ])
def index(request):

    return render(request, 'core/index.html')

@require_http_methods(['GET', ])
def calculateForm(request):

    return render(request, 'core/calculate.html')


@require_http_methods(['GET', 'POST', ])
def calculate(request, result=[]):

    if request.method == "POST":

        data = []
        temp = []

        n_size = int(request.GET.get('n'))

        for (count, i) in enumerate(list(request.POST.values())[1:], start=1):
            temp.append(int(i))

            if count % n_size == 0:
                data.append(temp.copy())
                temp.clear()

        result = functions.determinant(data)

        # this is the only way to redirect while also passing context
        request.method = "GET"  # to prevent infinite loop
        response = calculate(request, result=result)
        return response

    elif request.method == "GET":
        n = int(request.GET.get('n', 2))
        n_cells = range(n**2)  # the amount of input/cells

        return render(request, 'core/calculate.html', {
            'n': n,
            'n_cells': n_cells,
            'result': result
        })

@require_http_methods(['POST'])
def feedback(request):
    token = os.getenv("TOKEN")
    chat_id = os.getenv("CHAT_ID")

    # get post request from form html
    message = request.POST['feedback']

    # send message with telegram API
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
    if(requests.get(url)): 
        alert = {
            "text": "Terima kasih atas feedback Anda",
            "color": "text-blue-800",
            "backgroundColor": "bg-blue-50"
        }
    else:
        alert = {
            "text": "Gagal mengirimkan feedback, silahkan coba lagi!",
            "color": "text-red-800",
            "backgroundColor": "bg-red-50"
        }

    return render(request, 'core/index.html', {"alert": alert})