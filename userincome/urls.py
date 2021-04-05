from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import AddIncomeView, EditIncomeView, DeleteIncomeView,index_inc, CnfrmDeleteView, SearchView ,welcome_view

#app_name = 'expenses'
urlpatterns = [
    path('', welcome_view, name='welcome'),
    path('income/', index_inc, name='income'),
    path('income/add-income/', AddIncomeView.as_view(), name='add-income'),
    path('income/edit-income/<int:id>/', EditIncomeView.as_view(), name='edit-income'),
    path('income/delcnfrm-income/<int:id>/', CnfrmDeleteView.as_view(), name='delcnfrm-income'),
    path('income/delete-income/<int:id>', DeleteIncomeView.as_view(), name='delete-income'),
    path('income/search-income/', csrf_exempt(SearchView.as_view()), name='search-income')
]