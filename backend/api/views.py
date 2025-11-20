from rest_framework.decorators import api_view
from rest_framework.response import Response
import pandas as pd
from io import TextIOWrapper
from .models import EquipmentUpload

@api_view(['POST'])
def upload_equipment_data(request):
    file = request.FILES.get('file')
    if not file:
        return Response({'error': 'No file uploaded'}, status=400)

    try:
        df = pd.read_csv(TextIOWrapper(file, encoding='utf-8'))

        # Normalize columns
        df.columns = [col.strip().lower() for col in df.columns]

        summary = {
            'total_equipment': len(df),
            'average_flowrate': df['flowrate'].mean(),
            'average_pressure': df['pressure'].mean(),
            'average_temperature': df['temperature'].mean(),

            # IMPORTANT FIX:
            'type_distribution': df['type'].value_counts().to_dict()
        }

        # Save summary to DB
        EquipmentUpload.objects.create(
            filename=file.name,
            total_equipment=len(df),
            average_flowrate=df['flowrate'].mean(),
            average_pressure=df['pressure'].mean(),
            average_temperature=df['temperature'].mean()
        )

        # Keep last 5 uploads
        if EquipmentUpload.objects.count() > 5:
            oldest = EquipmentUpload.objects.order_by('upload_time').first()
            oldest.delete()

        return Response(summary)

    except Exception as e:
        return Response({'error': str(e)}, status=500)


@api_view(['GET'])
def get_upload_history(request):
    uploads = EquipmentUpload.objects.order_by('-upload_time')[:5]
    data = [
        {
            'filename': u.filename,
            'upload_time': u.upload_time.strftime("%Y-%m-%d %H:%M:%S"),
            'total_equipment': u.total_equipment,
            'average_flowrate': u.average_flowrate,
            'average_pressure': u.average_pressure,
            'average_temperature': u.average_temperature,
        }
        for u in uploads
    ]
    return Response(data)