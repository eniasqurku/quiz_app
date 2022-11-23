from django.urls import path

from common.views import download_daily_report

urlpatterns = [
    path('download_daily_report/', download_daily_report, name='daily_report')
]
