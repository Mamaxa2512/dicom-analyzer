"""
Module for parsing DICOM files using pydicom.
"""
# pyrefly: ignore [missing-import]
import pydicom
# pyrefly: ignore [missing-import]
import numpy as np
from PIL import Image




def parse_dicom(filepath: str) -> dict:
    dataset = pydicom.dcmread(filepath)
    return {'name': str(dataset.PatientName), 'age': dataset.PatientAge, 'sex': dataset.PatientSex, 'study_date': dataset.StudyDate, 'study_description': dataset.StudyDescription, 'modality': dataset.Modality}

def get_pixel_array(filepath: str):
    arr = pydicom.dcmread(filepath).pixel_array
    return arr
    

def get_image_as_png(filepath: str):
    arr = get_pixel_array(filepath)
    min = np.min(arr)
    max = np.max(arr)
    
    norm_arr = (arr - min) / (max - min)*255

    ready_arr = norm_arr.astype(np.uint8)

    img = Image.fromarray(ready_arr)
    return img
    
    
