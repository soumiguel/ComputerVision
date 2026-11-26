
import cv2

from vision.person_detector import PersonDetector
from events.event_manager import EventManager
from storage.image_storage import ImageStorage

from config import CAMERA_INDEX, WINDOW_NAME


def main():

    print("=" * 45)
    print("       ROOM VISION AI")
    print("=" * 45)

    # 1. Inicializa câmera

    camera = cv2.VideoCapture(CAMERA_INDEX)

    if not camera.isOpened():

        raise RuntimeError(
            "Não foi possível acessar a câmera."
        )

    # Aguarda estabilização da câmera

    for _ in range(30):
        camera.read()

    ret, baseline_frame = camera.read()

    if not ret:

        raise RuntimeError(
            "Falha ao capturar imagem inicial."
        )

    # 2. Inicializa IA

    detector = PersonDetector()

    # 3. Inicializa armazenamento

    storage = ImageStorage()

    # 4. Registra imagem de referência

    initial_detection = detector.detect(baseline_frame)

    if initial_detection["person_detected"]:

        camera.release()

        raise RuntimeError(
            "Pessoa detectada na inicialização. "
            "Deixe a sala vazia e reinicie."
        )

    storage.save_baseline(baseline_frame)

    # 5. Inicializa gerenciamento de eventos

    event_manager = EventManager()

    print("[SYSTEM] Sala vazia confirmada.")
    print("[SYSTEM] Monitoramento iniciado.")

    try:

        while True:

            ret, frame = camera.read()

            if not ret:
                break

            # Detecta pessoas

            detection = detector.detect(frame)

            # Atualiza gerenciamento de eventos

            event_manager.update(
                detection["person_detected"],
                frame
            )

            # Informações para visualização

            state = event_manager.get_state()

            display_frame = detection["frame"]

            cv2.putText(
                display_frame,
                f"STATE: {state}",
                (20, 35),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

            cv2.putText(
                display_frame,
                f"PEOPLE: {detection['person_count']}",
                (20, 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )

            cv2.imshow(
                WINDOW_NAME,
                display_frame
            )

            # Pressione Q para encerrar

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:

        camera.release()

        cv2.destroyAllWindows()

        print("[SYSTEM] Monitoramento encerrado.")


if __name__ == "__main__":

    main()
