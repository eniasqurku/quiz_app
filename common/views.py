from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from common.models import ActionLogger
import pandas as pd


@api_view(['POST'])
@permission_classes([IsAdminUser])
def download_daily_report(request):
    """
    Downloads daily report usage in csv form

    Body Parameter:
        date: str
    """
    date = request.data['date']
    logs = ActionLogger.objects.filter(action_time__date=date).values('change_message')
    if not logs.exists():
        Response(status=status.HTTP_204_NO_CONTENT)

    df = pd.DataFrame(logs)
    data = df['change_message'].value_counts()
    data = data.to_frame(name='Usage Nr')
    response = HttpResponse(content=data.to_csv(index_label='Type'), content_type="text/csv")
    response["Content-Disposition"] = f"attachment; filename=daily_usage_{date}.csv"

    return response
