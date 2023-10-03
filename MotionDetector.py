import cv2
import numpy as np

class MotionDetector:
    def __init__(self):
        self.back_frame = None
    
    def init_background(self, frame):
        self.back_frame = np.zeros_like(frame, np.float32)
    
    def detect(self, frame, threshold, thr=None):
        frame = frame.astype(np.float32)
        diff_frame = cv2.absdiff(frame, self.back_frame)
        cv2.accumulateWeighted(frame, self.back_frame, 0.025)
        diff = diff_frame.astype(np.uint8)
        gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        if thr is not None:
            _, gray_diff = cv2.threshold(gray_diff, thr, 255, cv2.THRESH_BINARY)
        bright = np.sum(gray_diff)
        color = (0, 0, 255) if bright > threshold else (255, 255, 0)
        gray_diff = cv2.cvtColor(gray_diff, cv2.COLOR_GRAY2BGR)
        cv2.rectangle(gray_diff, (50, 80), (125, 130), color, thickness=-1)
        return bright > threshold, gray_diff