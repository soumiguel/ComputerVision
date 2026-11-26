
from ultralytics import YOLO

from config import (
    MODEL_PATH,
    CONFIDENCE_THRESHOLD,
    IMAGE_SIZE
)


class PersonDetector:

    def __init__(self):

        print("[AI] Carregando modelo YOLO...")

        self.model = YOLO(MODEL_PATH)

        print("[AI] Modelo carregado!")

    def detect(self, frame):

        results = self.model.predict(
            source=frame,
            classes=[0],
            conf=CONFIDENCE_THRESHOLD,
            imgsz=IMAGE_SIZE,
            verbose=False
        )

        result = results[0]

        person_count = len(result.boxes)

        annotated_frame = result.plot()

        return {
            "person_detected": person_count > 0,
            "person_count": person_count,
            "frame": annotated_frame
        }
