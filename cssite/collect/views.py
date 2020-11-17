from django.shortcuts import render
from django.http import HttpResponse
from .models import Account

def index(request):
    account = Account.objects.get(pk=1)
    context = {
        'id': account.acc_id,
        'name': account.name,
    }
    return render(request, 'collect/index.html', {'context': context})
