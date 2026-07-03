from io import BytesIO

from django.http import HttpResponse
from django.shortcuts import render
from core.models import *
import pandas as pd
from django.http import StreamingHttpResponse

# Create your views here.
def chunk_generator(fh, chunk_size=8192):
    while True:
        chunk = fh.read(chunk_size)
        if not chunk:
            break
        yield chunk

## since we finally use google sheet, there is no need to generate a download api.

def export_students_from_db_to_excel(request):
    if request.method == 'GET':
        queryset = ApplicationStudent.objects.all()
        df_data = pd.DataFrame(list(queryset.values()))

    # Query reference data and convert it to a DataFrame
        reference_queryset = ApplicationStudentSubject.objects.all()
        df_reference_data = pd.DataFrame(list(reference_queryset.values()))

        # Create a Pandas Excel writer using ExcelWriter
        excel_file = BytesIO()
        with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
            # Write each DataFrame to a different worksheet
            df_data.to_excel(writer, sheet_name='Data', index=False)
            df_reference_data.to_excel(writer, sheet_name='ReferenceData', index=False)

        # Reset the BytesIO object to the beginning
        excel_file.seek(0)

        response = StreamingHttpResponse(chunk_generator(excel_file))
        response['Content-Disposition'] = 'attachment; filename="exported_data.xlsx"'
        return response
