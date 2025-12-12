from types import SimpleNamespace
from utils.gestures import is_pinch

def point(x, y):
    return SimpleNamespace(x=x, y=y)

def test_pinch():
    assert is_pinch(point(0.1, 0.1), point(0.12, 0.1), threshold=0.05)
    assert not is_pinch(point(0.1, 0.1), point(0.5, 0.5), threshold=0.05)
