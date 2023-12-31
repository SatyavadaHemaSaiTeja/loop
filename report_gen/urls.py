from django.urls import path
from .views import TriggerReportView, GetReportView

urlpatterns = [
    path('trigger_report/', TriggerReportView.as_view(), name='trigger_report'),
    path('get_report/<str:report_id>/', GetReportView.as_view(), name='get_report'),
]
