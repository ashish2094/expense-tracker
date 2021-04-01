from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.contrib import messages
from .models import Category, Expense
from django.views import View
from django.core.paginator import Paginator
import json
from django.http import JsonResponse


class SearchView(LoginRequiredMixin, View):
    login_url = '/auth/login/'
    def post(self, request):
        search_str = json.loads(request.body).get('searchText')
        expenses = Expense.objects.filter(amount__istartswith=search_str, owner=request.user) or Expense.objects.filter(
            date__istartswith=search_str, owner=request.user) or Expense.objects.filter(
                description__icontains=search_str, owner=request.user) or Expense.objects.filter(
                    category__icontains=search_str, owner=request.user)
        data = expenses.values()
        return JsonResponse(list(data), safe=False)

#@login_required(login_url='/auth/login/')
def welcome_view(request):
    context = {}
    return render(request, "index.html", context)

def index_view(request):
    data = []
    data = Expense.objects.filter(owner=request.user)
    p = Paginator(data, 4)
    page_no = request.GET.get('page')
    page_obj = Paginator.get_page(p, page_no)
    context = {
        'data': data,
        'page_obj' : page_obj
    }
    return render(request, "exp/index.html", context)


class AddExpenseView(LoginRequiredMixin, View):
    login_url = '/auth/login/'
    def get(self, request):
        categories = Category.objects.all()
        return render(request, "exp/add_expense.html", {'categories': categories})

    def post(self, request):
        amount = request.POST['amount']
        if not amount:
            messages.error(request, 'Amount Required')
            return redirect('/expenses/add-expense/')
        description = request.POST['description']
        category = request.POST['category']
        if not category:
            messages.error(request, 'Category Required')
            return redirect('/expenses/add-expense/')
        date = request.POST['date']
        Expense.objects.create(owner=request.user, amount = amount, description = description, 
            category = category, date = date)
        messages.info(request, 'Expense Added Successfully!')
        return redirect('/expenses/add-expense/')

class EditExpenseView(LoginRequiredMixin, View):
    login_url = '/auth/login/'
    def get(self, request, id):
        expense = Expense.objects.get(id=id)
        categories = Category.objects.all()
        context = {
            'categories': categories,
            'expense' : expense
            }
        return render(request, "exp/edit_exp.html", context)

    def post(self, request, id):
        amount = request.POST['amount']
        if not amount:
            messages.error(request, 'Amount Required')
            return redirect('/expenses/edit-expense/')
        description = request.POST['description']
        category = request.POST['category']
        date = request.POST['date']
        expense = Expense.objects.get(id=id)
        expense.owner=request.user
        expense.amount = amount
        expense.description = description
        expense.category = category
        expense.date = date
        expense.save()
        messages.info(request, 'Expense Updated Successfully!')
        return redirect('/expenses/')

class CnfrmDeleteView(LoginRequiredMixin, View):
    def get(self, request, id):
        return render(request, "partials/_popup.html", {"id":id})

class DeleteExpenseView(LoginRequiredMixin, View):
    def get(self, request, id):
        expense = Expense.objects.get(id=id)
        expense.delete()
        messages.info(request, 'Expense Deleted Successfully!')
        return redirect('/expenses/')