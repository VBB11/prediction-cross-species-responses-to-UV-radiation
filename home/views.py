from django.shortcuts import render
import numpy as np
from tensorflow.keras.models import load_model

model = load_model('./savedModels/Responses Model.h5', compile=False)

# Define class labels
class_labels = ['DNA damage', 'DNA repair', 'pathways', 'epigenetic', 'epigenetic']

def index(request):
    if request.method == 'POST':
        try:
            # Retrieve and convert inputs
            species = float(request.POST.get('species', '0'))
            organism = float(request.POST.get('organism', '0'))
            uv_type = float(request.POST.get('uv_type', '0'))
            exposure_intensity = float(request.POST.get('exposure_intensity', '0'))
            exposure_time = float(request.POST.get('exposure_time', '0'))
            organelle = float(request.POST.get('organelle', '0'))
            metabolites = float(request.POST.get('metabolites', '0'))
            proteins = float(request.POST.get('proteins', '0'))
            genes = float(request.POST.get('genes', '0'))
            studied_tissue = float(request.POST.get('studied_tissue', '0'))

            # Create input array
            input_data = np.array([[species, organism, uv_type, exposure_intensity, exposure_time, organelle, metabolites, proteins, genes, studied_tissue]])

             # Make prediction
            y_pred = model.predict(input_data)

            # Interpret prediction result
            if y_pred[0][0] == 0:
                y_pred = 'Signaling'
            elif y_pred[0][0] == 1:
                y_pred = 'Epigenetic'
            elif y_pred[0][0] == 2:
                y_pred = 'DNA Repair'
            elif y_pred[0][0] == 3:
                y_pred = 'Pathways'
            else:
                y_pred = 'DNA Damage'

            return render(request, 'home.html', {'result': y_pred})

        except ValueError as e:
            # Handle the case where input conversion fails
            return render(request, 'home.html', {'error': f'Invalid input data: {e}'})
    
    return render(request, 'home.html')
