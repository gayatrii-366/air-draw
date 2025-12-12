import math

def distance(p1, p2):
    """Euclidean distance between two points."""
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)


def is_pinch(index_tip, thumb_tip, threshold=0.04):
    """
    Detect pinch gesture based on distance between index fingertip and thumb fingertip.
    """
    return distance(index_tip, thumb_tip) < threshold


def is_clear_gesture(landmarks):
    """
    Detect 'clear' gesture.
    Simple version: if most fingers are folded.
    """
    folded = 0
    finger_tips = [8, 12, 16, 20]

    for tip in finger_tips:
        if landmarks[tip].y > landmarks[tip - 2].y:
            folded += 1

    return folded >= 3
