"""
Module for parsing DICOM files using pydicom.
"""
# pyrefly: ignore [missing-import]
import pydicom
# pyrefly: ignore [missing-import]
import numpy as np
from PIL import Image
from app import image_processor




def parse_dicom(filepath: str) -> dict:
    dataset = pydicom.dcmread(filepath)
    return {
        'name': str(getattr(dataset, 'PatientName', 'Unknown')),
        'age': str(getattr(dataset, 'PatientAge', 'Unknown')),
        'sex': str(getattr(dataset, 'PatientSex', 'Unknown')),
        'study_date': str(getattr(dataset, 'StudyDate', 'Unknown')),
        'study_description': str(getattr(dataset, 'StudyDescription', 'Unknown')),
        'modality': str(getattr(dataset, 'Modality', 'Unknown'))
    }

def get_pixel_array(filepath: str):
    arr = pydicom.dcmread(filepath).pixel_array
    return arr
    

def get_image_as_png(filepath: str):
    arr = get_pixel_array(filepath)
    min = np.min(arr)
    max = np.max(arr)
    
    norm_arr = (arr - min) / (max - min)*255

    ready_arr = norm_arr.astype(np.uint8)
    ready_arr = image_processor.upscale_for_display(ready_arr)

    img = Image.fromarray(ready_arr)
    return img
    
    
