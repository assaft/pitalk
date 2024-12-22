from abc import ABC, abstractmethod
from typing import Callable


class UIMainLoopAPI(ABC):

    @abstractmethod
    def set_ui_handlers(self,
                        on_record: Callable[[], None],
                        on_play: Callable[[], None],
                        on_next: Callable[[], None],
                        on_prev: Callable[[], None]):
        pass

    @abstractmethod
    def build_ui(self):
        pass

    @abstractmethod
    def set_recording(self, on: bool):
        pass

    @abstractmethod
    def set_playback(self, on: bool):
        pass

    @abstractmethod
    def start_rec_timer(self, ms: int, cb: Callable[[], None]):
        pass

    @abstractmethod
    def cancel_rec_timer(self):
        pass

    @abstractmethod
    def start_playback_timer(self, ms: int, cb: Callable[[], None]):
        pass

    @abstractmethod
    def cancel_playback_timer(self):
        pass

    @abstractmethod
    def run(self):
        pass
