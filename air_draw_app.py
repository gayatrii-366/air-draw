import cv2
import mediapipe as mp
import time
from draw_engine import AirDrawEngine
from utils.gestures import is_clear_gesture
from utils.fingers import is_index_up

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

# Drawing engine instance
engine = AirDrawEngine()

prev_time = 0

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)

cap = cv2.VideoCapture(0)
print("AirDraw running — Index finger = draw, fist = clear, C = colour, Q = quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    if engine.canvas is None:
        engine.initialise_canvas(frame)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    clear_active = False

    if results.multi_hand_landmarks:
        for hand in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

            # Index finger location
            index_tip = hand.landmark[8]
            point = (int(index_tip.x * w), int(index_tip.y * h))

            # Gesture checks
            draw_active = is_index_up(hand.landmark)
            clear_active = is_clear_gesture(hand.landmark)

            if draw_active:
                engine.draw(point, True)
            else:
                engine.prev_point = None  # stop smooth drawing

    # Clear gesture
    if clear_active:
        engine.clear_canvas()

    # Overlay
    output = engine.overlay(frame)

    # FPS counter
    curr_time = time.time()
    fps = int(1 / (curr_time - prev_time + 1e-6))
    prev_time = curr_time

    cv2.putText(
        output,
        f"FPS: {fps}",
        (w - 150, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    cv2.imshow("AirDraw", output)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('c'):
        engine.switch_colour()
    if key == ord('1'):
        engine.switch_colour(0)
    if key == ord('2'):
        engine.switch_colour(1)
    if key == ord('3'):
        engine.switch_colour(2)
    if key == ord('4'):
        engine.switch_colour(3)
    if key == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
