import streamlit as st
import cv2
import mediapipe as mp
from draw_engine import AirDrawEngine
from utils.fingers import is_index_up
from utils.gestures import is_clear_gesture

st.title("AirDraw – Hand Gesture Drawing App ✨")
st.write("Raise your index finger to draw. Make a fist to clear. Press C to change colour.")

run = st.checkbox("Start Camera")

mp_hands = mp.solutions.hands
engine = AirDrawEngine()
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)

camera = cv2.VideoCapture(0)
frame_placeholder = st.empty()

if run:
    while True:
        ret, frame = camera.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape

        if engine.canvas is None:
            engine.initialise_canvas(frame)

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        clear = False

        if results.multi_hand_landmarks:
            for hand in results.multi_hand_landmarks:
                index_tip = hand.landmark[8]
                point = (int(index_tip.x * w), int(index_tip.y * h))

                engine.draw(point, is_index_up(hand.landmark))

                if is_clear_gesture(hand.landmark):
                    clear = True

        if clear:
            engine.clear_canvas()

        output = engine.overlay(frame)
        frame_placeholder.image(output, channels="BGR")

camera.release()
