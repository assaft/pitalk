import uuid
import wave
from datetime import datetime, timezone
from pathlib import Path

import pyaudio


class Recorder:

    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1  # 1 if sys.platform == 'darwin' else 2,
    RATE = 44100

    BASE_PATH = Path("recordings")

    def __init__(self, eos_cb):
        self.frames = []
        self.p = None
        self.stream = None
        self.wf = None
        self.eos_cb = eos_cb

    def rec_callback(self, in_data, frame_count, time_info, status):
        self.frames.append(in_data)
        return in_data, pyaudio.paContinue

    def start_recording(self):
        self.frames = []
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.p.get_format_from_width(2),
                                  channels=self.CHANNELS, rate=self.RATE,
                                  frames_per_buffer=self.CHUNK,
                                  input=True, output=False,
                                  stream_callback=self.rec_callback)

    def stop_recording(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

        timestamp = datetime.now(timezone.utc).strftime('%Y_%m_%d-%H_%M_%S')
        filename = f"PT_{timestamp}_{uuid.uuid4()}.wav"
        path = self.BASE_PATH / filename
        with wave.open(str(path), 'wb') as wf:
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(b''.join(self.frames))

        self.reset()

        return path

    def play_callback(self, in_data, frame_count, time_info, status):
        data = self.wf.readframes(frame_count)
        # If len(data) is less than requested frame_count, PyAudio automatically
        # assumes the stream is finished, and the stream stops.
        if len(data) < frame_count * self.wf.getsampwidth():
            self.eos_cb() # notify end-of-stream is approaching
        return data, pyaudio.paContinue

    def start_playback(self, file_path):
        self.wf = wave.open(str(file_path), 'rb')
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.p.get_format_from_width(self.wf.getsampwidth()),
                                  channels=self.wf.getnchannels(),
                                  rate=self.wf.getframerate(),
                                  frames_per_buffer=self.CHUNK,
                                  input=False, output=True,
                                  stream_callback=self.play_callback)

    def stop_playback(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        self.wf.close()
        self.reset()

    def check_playback(self):
        return self.stream and self.stream.is_active()

    def reset(self):
        self.stream = None
        self.p = None
        self.wf = None