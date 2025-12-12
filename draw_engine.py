import numpy as np
import cv2

class AirDrawEngine:
    def __init__(self, colours=None, thickness=4, smooth_factor=0.2):
        self.canvas = None
        self.glow_canvas = None  # for neon blur
        self.prev_point = None
        self.colour_index = 0
        self.smooth_factor = smooth_factor
        self.smooth_point = None
        self.thickness = thickness

        self.colours = colours if colours else [
            (255, 0, 0),     # Blue
            (0, 255, 0),     # Green
            (0, 0, 255),     # Red
            (255, 255, 0)    # Cyan
        ]

    def initialise_canvas(self, frame):
        h, w, _ = frame.shape
        self.canvas = np.zeros((h, w, 3), dtype=np.uint8)
        self.glow_canvas = np.zeros((h, w, 3), dtype=np.uint8)

    def smooth(self, point):
        if self.smooth_point is None:
            self.smooth_point = point
        else:
            x = int(self.smooth_factor * point[0] + (1 - self.smooth_factor) * self.smooth_point[0])
            y = int(self.smooth_factor * point[1] + (1 - self.smooth_factor) * self.smooth_point[1])
            self.smooth_point = (x, y)
        return self.smooth_point

    def draw(self, point, active):
        point = self.smooth(point)

        if active:
            if self.prev_point is None:
                self.prev_point = point
                return

            colour = self.colours[self.colour_index]

            # Neon blur stroke
            cv2.line(self.glow_canvas, self.prev_point, point, colour, self.thickness * 4)

            # Sharp main stroke
            cv2.line(self.canvas, self.prev_point, point, colour, self.thickness)

            self.prev_point = point
        else:
            self.prev_point = None

    def clear_canvas(self):
        if self.canvas is not None:
            self.canvas[:] = 0
            self.glow_canvas[:] = 0
            print("Canvas cleared.")

    def switch_colour(self, index=None):
        if index is not None:
            self.colour_index = index
        else:
            self.colour_index = (self.colour_index + 1) % len(self.colours)
            print(f"Colour changed to index {self.colour_index}: {self.colours[self.colour_index]}")

    def overlay(self, frame):
        # Blur the glow layer for neon effect
        glow = cv2.GaussianBlur(self.glow_canvas, (21, 21), 0)

        # Mix layers
        combined = cv2.addWeighted(frame, 0.6, glow, 0.4, 0)
        combined = cv2.addWeighted(combined, 0.8, self.canvas, 0.9, 0)

        # App Title
        cv2.putText(
            combined,
            "AIR DRAW v1.0",
            (20, combined.shape[0] - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )

        # Show stroke thickness
        cv2.putText(
            combined,
            f"Thickness: {self.thickness}",
            (200, combined.shape[0] - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (200, 200, 200),
            2
        )

        # ==========================
        # DISPLAY COLOUR PALETTE (1–4)
        # ==========================

        start_x = 20
        start_y = 20
        box_size = 40
        gap = 15

        for i, colour in enumerate(self.colours):
            x1 = start_x + i * (box_size + gap)
            y1 = start_y
            x2 = x1 + box_size
            y2 = y1 + box_size

            # Draw colour box
            cv2.rectangle(combined, (x1, y1), (x2, y2), colour, -1)

            # Add number label
            cv2.putText(
                combined,
                str(i + 1),
                (x1 + 10, y2 + 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                colour,
                2
            )

            # Highlight the selected colour
            if i == self.colour_index:
                cv2.rectangle(combined, (x1 - 3, y1 - 3), (x2 + 3, y2 + 3), (255, 255, 255), 2)

        return combined

