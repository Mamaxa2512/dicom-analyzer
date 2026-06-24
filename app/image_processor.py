"""
Module for image processing operations.
"""
# pyrefly: ignore [missing-import]
from PIL import ImageMode
import typing_extensions
import typing_extensions
from PIL import ImageMode
# pyrefly: ignore [missing-import]
import numpy as np
# pyrefly: ignore [missing-import]
import cv2



def normalize(image_array):
    min = np.min(image_array)
    max = np.max(image_array)

    norm_arr = (image_array - min) / (max - min)*255
    img_8bit = norm_arr.astype(np.uint8)

    return img_8bit




def apply_window_level(image_array, window, level):
    min = level - window/2
    max = level + window/2
    cliped = np.clip(image_array, min, max)
    norm_arr = (cliped - min) / (max - min)*255
    return norm_arr.astype(np.uint8)


def apply_clahe(image_array):
    img_8bit = normalize(image_array)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))

    enhance_img = clahe.apply(img_8bit)

    return enhance_img


    

def apply_edge_detection(image_array):
    img_8bit = normalize(image_array)
    sobelx = cv2.Sobel(img_8bit,cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(img_8bit, cv2.CV_64F, 0, 1, ksize=3)
    magnitude = np.sqrt(sobelx**2 + sobely**2)
    final = np.clip(magnitude, 0, 255).astype(np.uint8)
    return final


def apply_invert(image_array):
    normalized = normalize(image_array)
    return 255 - normalized

