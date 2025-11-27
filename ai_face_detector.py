import numpy as np
from skimage import feature

def is_ai_generated_face(gray_face):
    try:
        lbp = feature.local_binary_pattern(gray_face, P=24, R=3, method="uniform")
        hist, _ = np.histogram(lbp.ravel(), bins=np.arange(0, 27), range=(0, 26))
        hist = hist.astype("float")
        hist /= (hist.sum() + 1e-7)
        return hist[0] > 0.5
    except Exception:
        return False
