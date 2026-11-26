
from enum import Enum

from config import (
    FRAMES_TO_ENTER,
    FRAMES_TO_EXIT
)

from storage.image_storage import ImageStorage


class RoomState(Enum):

    EMPTY = "EMPTY"
    ENTERING = "ENTERING"
    OCCUPIED = "OCCUPIED"
    EXITING = "EXITING"


class EventManager:

    def __init__(self):

        self.storage = ImageStorage()

        self.state = RoomState.EMPTY

        self.enter_counter = 0
        self.exit_counter = 0

        self.first_frame = None
        self.last_frame = None

    def update(self, person_detected, frame):

        # -------------------------
        # SALA VAZIA
        # -------------------------

        if self.state == RoomState.EMPTY:

            if person_detected:

                self.state = RoomState.ENTERING

                self.enter_counter = 1
                self.first_frame = frame.copy()

        # -------------------------
        # CONFIRMANDO ENTRADA
        # -------------------------

        elif self.state == RoomState.ENTERING:

            if person_detected:

                self.enter_counter += 1

                if self.enter_counter >= FRAMES_TO_ENTER:

                    self.storage.save_event_frame(
                        self.first_frame,
                        "ENTRY"
                    )

                    self.state = RoomState.OCCUPIED

                    print("[EVENT] Entrada confirmada!")

            else:

                self.state = RoomState.EMPTY

                self.enter_counter = 0
                self.first_frame = None

        # -------------------------
        # SALA OCUPADA
        # -------------------------

        elif self.state == RoomState.OCCUPIED:

            if not person_detected:

                self.state = RoomState.EXITING

                self.exit_counter = 1
                self.last_frame = frame.copy()

        # -------------------------
        # CONFIRMANDO SAIDA
        # -------------------------

        elif self.state == RoomState.EXITING:

            if not person_detected:

                self.exit_counter += 1

                if self.exit_counter >= FRAMES_TO_EXIT:

                    self.storage.save_event_frame(
                        self.last_frame,
                        "EXIT"
                    )

                    print("[EVENT] Saída confirmada!")

                    self.state = RoomState.EMPTY

                    self.enter_counter = 0
                    self.exit_counter = 0

                    self.first_frame = None
                    self.last_frame = None

            else:

                self.state = RoomState.OCCUPIED

                self.exit_counter = 0
                self.last_frame = None

    def get_state(self):

        return self.state.value
