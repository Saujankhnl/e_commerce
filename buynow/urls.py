from django.urls import path
from . import views
app_name = 'buynow'

urlpatterns = [
    path('buy_now/', views.buy_now, name='buy_now'),
]