from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.contrib import messages
from .models import Source, Income
from userpref.models import UserPref
from django.views import View
from django.core.paginator import Paginator
import json
from django.http import JsonResponse


class SearchView(LoginRequiredMixin, View):
    login_url = '/auth/login/'
    def post(self, request):
        search_str = json.loads(request.body).get('searchText')
        income = Income.objects.filter(amount__istartswith=search_str, owner=request.user) or Income.objects.filter(
            date__istartswith=search_str, owner=request.user) or Income.objects.filter(
                description__icontains=search_str, owner=request.user) or Income.objects.filter(
                    source__icontains=search_str, owner=request.user)
        data = income.values()
        return JsonResponse(list(data), safe=False)

#@login_required(login_url='/auth/login/')
def welcome_view(request):
    context = {}
    return render(request, "index.html", context)
    
def index_inc(request):
    data = []
    data = Income.objects.filter(owner=request.user)
    currency = UserPref.objects.get(user=request.user).currency
    p = Paginator(data, 4)
    page_no = request.GET.get('page')
    page_obj = Paginator.get_page(p, page_no)
    context = {
        'data': data,
        'page_obj' : page_obj,
        'currency' : currency
    }
    return render(request, "inc/index.html", context)


class AddIncomeView(LoginRequiredMixin, View):
    login_url = '/auth/login/'
    def get(self, request):
        source = Source.objects.all()
        currency = UserPref.objects.get(user=request.user).currency
        context = {
            'sources': source,
            'currency' : currency
            }
        return render(request, "inc/add_income.html", context)

    def post(self, request):
        amount = request.POST['amount']
        if not amount:
            messages.error(request, 'Amount Required')
            return redirect('/income/add-income/')
        description = request.POST['description']
        source = request.POST['source']
        if not source:
            messages.error(request, 'Source Required')
            return redirect('/income/add-income/')
        date = request.POST['date']
        Income.objects.create(owner=request.user, amount = amount, description = description, 
            source = source, date = date)
        messages.info(request, 'Income Added Successfully!')
        return redirect('/income/add-income/')

class EditIncomeView(LoginRequiredMixin, View):
    login_url = '/auth/login/'
    def get(self, request, id):
        income = Income.objects.get(owner=request.user, pk=id)
        source = Source.objects.all()
        currency = UserPref.objects.get(user=request.user).currency
        context = {
            'sources': source,
            'income' : income,
            'currency' : currency
            }
        return render(request, "inc/edit_income.html", context)

    def post(self, request, id):
        amount = request.POST['amount']
        if not amount:
            messages.error(request, 'Amount Required')
            return redirect('income/edit-income/')
        description = request.POST['description']
        source = request.POST['source']
        date = request.POST['date']
        income = Income.objects.get(id=id)
        income.owner=request.user
        income.amount = amount
        income.description = description
        income.source = source
        income.date = date
        income.save()
        messages.info(request, 'Income Updated Successfully!')
        return redirect('/income/')

class CnfrmDeleteView(LoginRequiredMixin, View):
    def get(self, request, id):
        return render(request, "inc/delete_inc.html", {"id":id})

class DeleteIncomeView(LoginRequiredMixin, View):
    def get(self, request, id):
        income = Income.objects.get(id=id)
        income.delete()
        messages.info(request, 'Income Deleted Successfully!')
        return redirect('/income/')