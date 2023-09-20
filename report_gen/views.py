from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from celery.result import AsyncResult
from .uptime_calculator import generate_report
from .serializers import ReportSerializer
from loop.loop_assignment.celery import app


@app.task(bind=True)
def generate_report_task(self):
    # Logic to generate report
    report_data = generate_report()
    return report_data


class TriggerReportView(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        task = generate_report_task.apply_async()
        return Response({"report_id": task.id}, status=status.HTTP_201_CREATED)


class GetReportView(APIView):
    @staticmethod
    def get(request, report_id, *args, **kwargs):
        task = AsyncResult(report_id)
        if task.state == 'PENDING':
            return Response({"status": "Running"}, status=status.HTTP_200_OK)
        elif task.state != 'FAILURE':
            serializer = ReportSerializer(task.result, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"status": "Error generating report"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
