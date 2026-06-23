"""
Module for parsing DICOM files using pydicom.
"""
import pydicom


def parse_dicom(filepath: str) -> dict:
    dataset = pydicom.dcmread(filepath)
    return {'name': str(dataset.PatientName), 'age': dataset.PatientAge, 'sex': dataset.PatientSex, 'study_date': dataset.StudyDate, 'study_description': dataset.StudyDescription}

def get_pixel_array(filepath: str):
    """
    Extract pixel data from DICOM.
    TODO: Phase 1 - Implement
    """
    pass

def get_image_as_png(filepath: str):
    """
    Convert DICOM pixel data to PNG for web display.
    TODO: Phase 1 - Implement
    """
    pass
