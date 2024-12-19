import tkinter as tk
from collections import defaultdict
from collections.abc import Callable
from enum import Enum
from tkinter import TOP, LEFT, RIGHT, BOTTOM
from typing import List


class UIEvent(Enum):
    INIT = "init"
    RECORD_PRESSED = "record_pressed",
    RECORD_ENDED = "record_ended",
    PLAY_PRESSED = "play_pressed",
    PLAY_ENDED = "play_ended",
    NEXT_PRESSED = "next_pressed",
    NAME_STARTED = "name_started",
    NAME_ENDED = "name_ended"


class UIState(Enum):
    INIT = "init",
    READY = "ready",
    RECORDING = "recording",
    PLAYING = "playing"
    ANNOUNCING = "announcing"


Action = Callable[[UIState, UIState], None]


class Transition:

    def __init__(self, source: UIState, event: UIEvent,
                 target: UIState, action: Action | List[Action]):
        self.source = source
        self.target = target
        self.action = action
        self.event = event


class StateMachine:

    def __init__(self):
        self.current_state = None
        self.transitions = defaultdict(list)

    def create(self, start: UIState, transitions: List[Transition]):
        self.current_state = start
        for t in transitions:
            self.transitions[t.source].append(t)

    def execute(self, event: UIEvent):
        for t in self.transitions[self.current_state]:
            if t.event == event:
                prev_state = self.current_state
                self.current_state = t.target
                if isinstance(t.action, list):
                    for action in t.action:
                        action(prev_state, t.target)
                else:
                    t.action(prev_state, t.target)
                return

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

def build_ui(_current_state: UIState, _next_state: UIState):
    ui.create()

def start_recording(current_state: UIState, next_state: UIState):
    ui.rec_box.config(background="blue")
    ui.rec_button.config(text="Recording")
    ui.rec_timer = ui.r.after(5000, lambda: state_machine.execute(UIEvent.RECORD_ENDED))

def stop_recording(current_state: UIState, next_state: UIState):
    ui.rec_box.config(background="green")
    ui.rec_button.config(text="Record")
    ui.r.after_cancel(ui.rec_timer)

def start_playing(current_state: UIState, next_state: UIState):
    ui.play_box.config(background="blue")
    ui.play_button.config(text="Playing")
    ui.play_timer = ui.r.after(5000, lambda: state_machine.execute(UIEvent.PLAY_PRESSED))

def stop_playing(current_state: UIState, next_state: UIState):
    ui.play_box.config(background="green")
    ui.play_button.config(text="Play")
    ui.r.after_cancel(ui.play_timer)

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
        Transition(UIState.PLAYING, UIEvent.PLAY_ENDED, UIState.READY, stop_playing),
        Transition(UIState.PLAYING, UIEvent.RECORD_PRESSED, UIState.RECORDING,
                   [stop_playing, start_recording]),

        # Transition(UIState.READY, UIEvent.PLAY_PRESSED, UIState.PLAYING, start_playing),
        # Transition(UIState.READY, UIEvent.PLAY_ENDED, UIState.READY, stop_playing),
    ]

    state_machine.create(start=UIState.INIT, transitions=transitions)
    state_machine.execute(event=UIEvent.INIT)


if __name__ == '__main__':
    main()
