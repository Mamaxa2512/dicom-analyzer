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



def get_histogram(image_array):
    img_norm = normalize(image_array)
    hist = cv2.calcHist([img_norm], [0], None, [256], [0, 256])
    return hist.flatten().tolist()

def upscale_for_display(image_8bit, min_size = 512):
    h, w = image_8bit.shape[:2]
    if h < min_size or w < min_size:
        scale = max(min_size/h, min_size/w)
        new_size = (int(w*scale), int(h*scale))
        return cv2.resize(image_8bit, new_size, interpolation = cv2.INTER_CUBIC)
    return image_8bit