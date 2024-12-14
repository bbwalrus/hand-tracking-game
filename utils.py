# utils.py

import cv2

def prepare_frame(frame):
    return cv2.flip(frame, 1)

def convert_to_rgb(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
