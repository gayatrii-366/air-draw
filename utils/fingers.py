def is_index_up(landmarks):
    """
    Returns True if the index finger is raised (tip above pip joint).
    landmarks: mediapipe hand.landmark list
    """
    tip = landmarks[8]
    pip = landmarks[6]

    return tip.y < pip.y     # smaller y = higher finger because origin is top-left
