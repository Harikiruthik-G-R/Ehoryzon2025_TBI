from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('funds/', funds, name='funds'),
    path('incubation/', incub, name='incub'),
    path('form/', form_view, name='form'),
    path('moments/', newspc, name='newspc'),
    path('montor/', mentor, name='mentor'),
    path('recents/', recents, name='recent'),
    path('product/', products, name='product'),
    path("spark-fund/", spark_fund_form, name="spark_fund_form"),
    path("api/applications/", get_applications, name="get_applications"),
]
