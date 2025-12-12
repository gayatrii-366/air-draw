import cv2
import mediapipe as mp
from utils.gestures import is_pinch, is_clear_gesture

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)

def point_from_landmark(landmark, w, h):
    return type("Point", (), {"x": landmark.x, "y": landmark.y})

cap = cv2.VideoCapture(0)
print("Running Gesture Test... Press 'q' to quit.")

while True:
    success, frame = cap.read()
    if not success:
        print("Camera error.")
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    gesture_text = "No gesture detected"

    if results.multi_hand_landmarks:
        for hand in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

            index_tip = hand.landmark[8]
            thumb_tip = hand.landmark[4]

            pt_index = point_from_landmark(index_tip, w, h)
            pt_thumb = point_from_landmark(thumb_tip, w, h)

            if is_pinch(pt_index, pt_thumb, threshold=0.04):
                gesture_text = "PINCH detected"
            elif is_clear_gesture(hand.landmark):
                gesture_text = "CLEAR gesture detected"

    cv2.putText(frame, gesture_text, (10, 40), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 255, 0), 2)

    cv2.imshow("Gesture Test", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
