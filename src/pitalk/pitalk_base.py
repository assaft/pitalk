import logging
from collections import defaultdict
from enum import Enum
from typing import Callable, List

from pitalk.audio_api.audio_api_base import AudioAPI
from pitalk.ui_mainloop_api.ui_mainloop_api_base import UIMainLoopAPI
from pitalk.user_api import User

logger = logging.getLogger(__name__)


class UIEvent(Enum):
    INIT = "init"
    RECORD_PRESSED = "record_pressed",
    RECORD_ENDED = "record_ended",
    PLAY_PRESSED = "play_pressed",
    PLAY_ENDED = "play_ended",
    PLAY_NEAR_EOS = "play_near_eos",
    NEXT_PRESSED = "next_pressed",
    PREV_PRESSED = "prev_pressed",
    NAME_STARTED = "name_started",
    NAME_ENDED = "name_ended"


class UIState(Enum):
    INIT = "init"
    READY = "ready"
    RECORDING = "recording"
    PLAYING = "playing"
    MONITORING = "monitoring"
    ANNOUNCING = "announcing"

Action = Callable[[], None]


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
                logger.debug(f"state update: {self.current_state} => {t.target}")
                prev_state = self.current_state
                self.current_state = t.target
                if isinstance(t.action, list):
                    for action in t.action:
                        action()
                else:
                    t.action()
                logger.debug(f"state updated.")
                return


class PITalk:

    def __init__(self, ui_mainloop_api: UIMainLoopAPI, audio_api: AudioAPI, user_name: str):
        self.ui_mainloop_api = ui_mainloop_api
        self.audio_api = audio_api
        self.file_path = None
        self.state_machine = StateMachine()
        self.user_name = user_name
        self.user = User(user_name)
        self.friend_id = 0

        transitions = [
            Transition(UIState.INIT, UIEvent.INIT, UIState.READY, self.build_ui),

            Transition(UIState.READY, UIEvent.RECORD_PRESSED, UIState.RECORDING, self.start_recording),
            Transition(UIState.READY, UIEvent.PLAY_PRESSED, UIState.PLAYING, self.start_playing),
            Transition(UIState.READY, UIEvent.NEXT_PRESSED, UIState.PLAYING,
                       [self.move_next, self.start_announcing]),
            Transition(UIState.READY, UIEvent.PREV_PRESSED, UIState.PLAYING,
                       [self.move_previous, self.start_announcing]),

            Transition(UIState.RECORDING, UIEvent.RECORD_PRESSED, UIState.READY, self.stop_recording),
            Transition(UIState.RECORDING, UIEvent.RECORD_ENDED, UIState.READY, self.stop_recording),
            Transition(UIState.RECORDING, UIEvent.PLAY_PRESSED, UIState.PLAYING,
                       [self.stop_recording, self.start_playing]),

            Transition(UIState.PLAYING, UIEvent.PLAY_PRESSED, UIState.READY, self.stop_playing),
            Transition(UIState.PLAYING, UIEvent.RECORD_PRESSED, UIState.RECORDING,
                       [self.stop_playing, self.start_recording]),
            Transition(UIState.PLAYING, UIEvent.PLAY_NEAR_EOS, UIState.MONITORING, self.monitor_playback),

            Transition(UIState.MONITORING, UIEvent.PLAY_ENDED, UIState.READY, self.stop_playing),
            Transition(UIState.MONITORING, UIEvent.PLAY_NEAR_EOS, UIState.MONITORING, self.monitor_playback),
        ]




        self.ui_mainloop_api.set_ui_handlers(
            on_record=lambda: self.state_machine.execute(UIEvent.RECORD_PRESSED),
            on_play=lambda: self.state_machine.execute(UIEvent.PLAY_PRESSED),
            on_next=lambda: self.state_machine.execute(UIEvent.NEXT_PRESSED),
            on_prev=lambda: self.state_machine.execute(UIEvent.PREV_PRESSED),
        )

        self.audio_api.set_audio_handlers(
            on_eos=lambda: self.state_machine.execute(UIEvent.PLAY_NEAR_EOS)
        )

        self.state_machine.create(start=UIState.INIT,
                                  transitions=transitions)


    def build_ui(self):
        logger.debug("build_ui()")
        self.ui_mainloop_api.build_ui()

    def start_recording(self):
        logger.debug("start_recording()")
        self.ui_mainloop_api.set_recording(on=True)
        self.ui_mainloop_api.start_rec_timer(
            5000, lambda: self.state_machine.execute(UIEvent.RECORD_ENDED))
        self.audio_api.start_recording()

    def stop_recording(self):
        logger.debug("stop_recording()")
        self.ui_mainloop_api.set_recording(on=False)
        self.ui_mainloop_api.cancel_rec_timer()
        self.file_path = self.audio_api.stop_recording()

    def start_playing(self):
        logger.debug("start_playing")
        self.ui_mainloop_api.set_playback(on=True)
        self.audio_api.start_playback(path=self.file_path)

    def stop_playing(self):
        logger.debug("stop_playing")
        self.ui_mainloop_api.set_playback(on=False)
        self.audio_api.stop_playback()
        self.ui_mainloop_api.cancel_playback_timer()

    def monitor_playback(self):
        logger.debug("monitor_playback")
        if self.audio_api.is_playback_active():
            self.ui_mainloop_api.start_playback_timer(
                100, lambda: self.state_machine.execute(UIEvent.PLAY_NEAR_EOS))
        else:
            self.state_machine.execute(UIEvent.PLAY_ENDED)

    def move_next(self):
        self.friend_id = (self.friend_id + 1) % len(self.user.friend_list)

    def move_previous(self):
        self.friend_id = (self.friend_id - 1) % len(self.user.friend_list)

    def start_announcing(self):
        logger.debug("start_announcing")
        friend_card = self.user.friend_list[self.friend_id]
        wav_data = friend_card.announce_data
        self.audio_api.start_playback(wav_data=wav_data)

    def run(self):
        self.state_machine.execute(event=UIEvent.INIT)
        self.ui_mainloop_api.run()
