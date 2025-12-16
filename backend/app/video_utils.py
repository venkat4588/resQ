import cv2
import numpy as np

def compute_deformation(frame1, frame2):
    """
    Quantify vehicle deformation between two frames.
    Returns a float deformation value.
    """
    try:
        gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        diff = cv2.absdiff(gray1, gray2)
        score = np.sum(diff) / diff.size  # Mean pixel difference
        return score
    except Exception as e:
        print("Deformation error:", str(e))
        return 0.0

def estimate_speed(frames):
    """
    Estimate speed using optical flow between first and last frames in sequence.
    Returns mean flow magnitude.
    """
    try:
        if len(frames) < 2:
            return 0.0
        prev = cv2.cvtColor(frames[0], cv2.COLOR_BGR2GRAY)
        curr = cv2.cvtColor(frames[-1], cv2.COLOR_BGR2GRAY)
        flow = cv2.calcOpticalFlowFarneback(prev, curr, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
        mean_mag = float(np.mean(mag))
        return mean_mag
    except Exception as e:
        print("Speed estimation error:", str(e))
        return 0.0
