from abc import ABC, abstractmethod
from pathlib import Path


class AudioAPI(ABC):

    @abstractmethod
    def set_audio_handlers(self, on_eos):
        pass

    @abstractmethod
    def start_recording(self):
        pass

    @abstractmethod
    def stop_recording(self) -> Path:
        pass

    @abstractmethod
    def start_playback(self, path: Path):
        pass

    @abstractmethod
    def stop_playback(self):
        pass

    @abstractmethod
    def is_playback_active(self):
        pass
