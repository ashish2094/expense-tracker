from django.shortcuts import render , redirect
import os
import json
from django.views import View
from django.conf import settings
from .models import UserPref
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.
#@login_required(login_url='/auth/login/')
class IndexView(View):
    def get(self, request):

        exist = UserPref.objects.filter(user=request.user).exists() #gives true or false
        if exist:
            user_pref = UserPref.objects.get(user=request.user)
        else:
            user_pref =  'null'
        currency_data = []
        file_path = os.path.join(settings.BASE_DIR, 'currencies.json')#getting the file path of json

        with open(file_path, 'r') as json_file: #converting data of json file to python list
            data = json.load(json_file)
            for k,v in data.items():
                currency_data.append({'name':k, 'value': v})
            
            #import pdb #python debugger, its going to pause the prgrm and check for data
            #pdb.set_trace()
        return render(request, 'prefrences/index.html', {'currencies': currency_data ,'user_pref': user_pref})
        
    def post(self, request):
        exist = UserPref.objects.filter(user=request.user).exists()
        currency = request.POST['currency']
        if exist:
            user_pref = UserPref.objects.get(user=request.user)    
            user_pref.currency = currency
            user_pref.save()
        else:
            UserPref.objects.create(user=request.user, currency = currency)
        messages.info(request, 'Currency Changed')
        return redirect('/prefrences/general/')