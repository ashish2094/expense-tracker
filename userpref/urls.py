from django.urls import path
from .views import IndexView

#app_name = 'userpref'
urlpatterns = [
    path('general/', IndexView.as_view(), name='general-prefrence'),
    #path('account/', account, name='account-prefrence'),
    
]