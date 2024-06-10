from django.shortcuts import render
from .forms import UploadFileForm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64
import os

def handle_uploaded_file(f):
    with open('temp.csv', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return pd.read_csv('temp.csv')

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            df = handle_uploaded_file(request.FILES['file'])
            
            # Basic Data Analysis
            summary_stats = df.describe().to_html()
            head = df.head().to_html()
            
            # Handle missing values
            df.fillna(0, inplace=True)
            
            # Visualization
            plt.figure(figsize=(10, 6))
            sns.histplot(df.select_dtypes(include=[np.number]))
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            image_png = buffer.getvalue()
            buffer.close()
            image_base64 = base64.b64encode(image_png).decode('utf-8')

            return render(request, 'result.html', {
                'head': head,
                'summary_stats': summary_stats,
                'image_base64': image_base64
            })
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})