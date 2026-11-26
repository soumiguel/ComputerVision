
import cv2
import os

from datetime import datetime

from config import CAPTURE_DIR, BASELINE_PATH


class ImageStorage:

    def __init__(self):

        os.makedirs(CAPTURE_DIR, exist_ok=True)

        os.makedirs(
            os.path.dirname(BASELINE_PATH),
            exist_ok=True
        )

    def save_baseline(self, frame):

        cv2.imwrite(BASELINE_PATH, frame)

        print(f"[STORAGE] Referência salva: {BASELINE_PATH}")

    def save_event_frame(self, frame, event_type):

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S_%f"
        )

        filename = f"{timestamp}_{event_type}.jpg"

        filepath = os.path.join(
            CAPTURE_DIR,
            filename
        )

        cv2.imwrite(filepath, frame)

        print(f"[STORAGE] Imagem salva: {filepath}")

        return filepath
