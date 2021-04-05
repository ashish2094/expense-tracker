from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import AddExpenseView, EditExpenseView, DeleteExpenseView, welcome_view,index_view, CnfrmDeleteView, SearchView

#app_name = 'expenses'
urlpatterns = [
    path('', welcome_view, name='welcome'),
    path('expenses/', index_view, name='expense'),
    path('expenses/add-expense/', AddExpenseView.as_view(), name='add-expense'),
    path('expenses/edit-expense/<int:id>/', EditExpenseView.as_view(), name='edit-expense'),
    path('expenses/delcnfrm-expense/<int:id>/', CnfrmDeleteView.as_view(), name='delcnfrm-expense'),
    path('expenses/delete-expense/<int:id>', DeleteExpenseView.as_view(), name='delete-expense'),
    path('expenses/search-expense/', csrf_exempt(SearchView.as_view()), name='search-expense')
]