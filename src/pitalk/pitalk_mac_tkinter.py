from pitalk.pitalk_base import PITalk
from pitalk.audio_api.audio_api_mac import PyAudioAPI
from pitalk.ui_mainloop_api.ui_mainloop_api_tkinter import TkinterUI
from pitalk.utils import init_logger


def main():
    init_logger()
    pi_talk = PITalk(ui_mainloop_api=TkinterUI(),
                     audio_api=PyAudioAPI())
    pi_talk.run()


if __name__ == '__main__':
    main()
