import logging
import tkinter as tk
from tkinter import TOP, LEFT, RIGHT, BOTTOM

from audio_api_2 import Recorder
from state_machine import UIEvent, UIState, Transition, StateMachine
from utils import init_logger

init_logger()

logger = logging.getLogger(__name__)

state_machine = StateMachine()


class UIControls:
    def __init__(self):
        self.r = None
        self.rec_box = None
        self.rec_button = None
        self.rec_timer = None
        self.play_box = None
        self.play_button = None
        self.play_timer = None

    def create(self):
        self.r = tk.Tk()
        self.r.title('PiTalk GUI')

        rec_frame = tk.Frame(self.r)
        rec_frame.pack(side=LEFT)

        play_frame = tk.Frame(self.r)
        play_frame.pack(side=RIGHT)

        self.rec_box = tk.Text(self.r, background="green", width=20, height=10)
        self.rec_box.pack(in_=rec_frame, side=TOP)
        self.rec_button = tk.Button(self.r, text='Record', width=25,
                                    command=lambda: state_machine.execute(
                                        event=UIEvent.RECORD_PRESSED))
        self.rec_button.pack(in_=rec_frame, side=BOTTOM)
        
        self.play_box = tk.Text(self.r, background="green", width=20, height=10)
        self.play_box.pack(in_=play_frame, side=TOP)
        self.play_button = tk.Button(self.r, text='Play', width=25,
                                     command=lambda: state_machine.execute(
                                        event=UIEvent.PLAY_PRESSED))
        self.play_button.pack(in_=play_frame, side=BOTTOM)

        self.r.mainloop()

ui = UIControls()
rec = Recorder(eos_cb=lambda: state_machine.execute(UIEvent.PLAY_NEAR_EOS))
files = []

def build_ui(_current_state: UIState, _next_state: UIState):
    ui.create()

def start_recording(current_state: UIState, next_state: UIState):
    logger.debug("start_recording()")

    ui.rec_box.config(background="blue")
    ui.rec_button.config(text="Recording")
    ui.rec_timer = ui.r.after(5000, lambda: state_machine.execute(UIEvent.RECORD_ENDED))
    rec.start_recording()

def stop_recording(current_state: UIState, next_state: UIState):
    logger.debug("stop_recording()")

    ui.rec_box.config(background="green")
    ui.rec_button.config(text="Record")
    if ui.rec_timer:
        ui.r.after_cancel(ui.rec_timer)
        ui.rec_timer = None
    file_path = rec.stop_recording()
    files.append(file_path)

def start_playing(current_state: UIState, next_state: UIState):
    logger.debug("start_playing")

    ui.play_box.config(background="blue")
    ui.play_button.config(text="Playing")
    # ui.play_timer = ui.r.after(5000, lambda: state_machine.execute(UIEvent.PLAY_PRESSED))
    rec.start_playback(files[-1])

def stop_playing(current_state: UIState, next_state: UIState):
    logger.debug("stop_playing")

    ui.play_box.config(background="green")
    ui.play_button.config(text="Play")
    rec.stop_playback()
    if ui.play_timer:
        ui.r.after_cancel(ui.play_timer)
        ui.play_timer = None

def monitor_playing(current_state: UIState, next_state: UIState):
    logger.debug("monitor_playback")
    if not rec.check_playback():
        logger.debug("stream ended")
        state_machine.execute(UIEvent.PLAY_ENDED)
    else:
        logger.debug("scheduling another monitor")
        ui.play_timer = ui.r.after(100, lambda: monitor_playing(current_state, next_state))

def main():
    transitions = [
        Transition(UIState.INIT, UIEvent.INIT, UIState.READY, build_ui),

        Transition(UIState.READY, UIEvent.RECORD_PRESSED, UIState.RECORDING, start_recording),
        Transition(UIState.READY, UIEvent.PLAY_PRESSED, UIState.PLAYING, start_playing),

        Transition(UIState.RECORDING, UIEvent.RECORD_PRESSED, UIState.READY, stop_recording),
        Transition(UIState.RECORDING, UIEvent.RECORD_ENDED, UIState.READY, stop_recording),
        Transition(UIState.RECORDING, UIEvent.PLAY_PRESSED, UIState.PLAYING,
                   [stop_recording, start_playing]),

        Transition(UIState.PLAYING, UIEvent.PLAY_PRESSED, UIState.READY, stop_playing),
        Transition(UIState.PLAYING, UIEvent.RECORD_PRESSED, UIState.RECORDING,
                   [stop_playing, start_recording]),
        Transition(UIState.PLAYING, UIEvent.PLAY_NEAR_EOS, UIState.MONITORING, monitor_playing),
        Transition(UIState.MONITORING, UIEvent.PLAY_ENDED, UIState.READY, stop_playing),

        # Transition(UIState.READY, UIEvent.PLAY_PRESSED, UIState.PLAYING, start_playing),
        # Transition(UIState.READY, UIEvent.PLAY_ENDED, UIState.READY, stop_playing),
    ]

    state_machine.create(start=UIState.INIT, transitions=transitions)
    state_machine.execute(event=UIEvent.INIT)


if __name__ == '__main__':
    main()
