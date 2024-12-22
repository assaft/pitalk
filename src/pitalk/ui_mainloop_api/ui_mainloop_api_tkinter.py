import tkinter as tk
from tkinter import TOP, LEFT, RIGHT, BOTTOM
from typing import Callable

from pitalk.ui_mainloop_api.ui_mainloop_api_base import UIMainLoopAPI


class TkinterUI(UIMainLoopAPI):

    def __init__(self):
        self.r = None
        self.next_button = None
        self.prev_button = None
        self.rec_box = None
        self.rec_button = None
        self.rec_timer = None
        self.play_box = None
        self.play_button = None
        self.play_timer = None
        self.on_record = None
        self.on_play = None
        self.on_next = None
        self.on_prev = None

    def set_ui_handlers(self,
                        on_record: Callable[[], None],
                        on_play: Callable[[], None],
                        on_next: Callable[[], None],
                        on_prev: Callable[[], None]):
        self.on_record = on_record
        self.on_play = on_play
        self.on_next = on_next
        self.on_prev = on_prev

    def build_ui(self):
        self.r = tk.Tk()
        self.r.title('PiTalk GUI')

        nav_frame = tk.Frame(self.r)
        nav_frame.pack(side=LEFT)

        rec_frame = tk.Frame(self.r)
        rec_frame.pack(side=LEFT)

        play_frame = tk.Frame(self.r)
        play_frame.pack(side=RIGHT)

        self.next_button = tk.Button(self.r, text='Next', width=25, command=self.on_next)
        self.next_button.pack(in_=nav_frame, side=TOP)
        self.prev_button = tk.Button(self.r, text='Prev', width=25, command=self.on_prev)
        self.prev_button.pack(in_=nav_frame, side=BOTTOM)

        self.rec_box = tk.Text(self.r, background="green", width=20, height=10)
        self.rec_box.pack(in_=rec_frame, side=TOP)
        self.rec_button = tk.Button(self.r, text='Record', width=25, command=self.on_record)
        self.rec_button.pack(in_=rec_frame, side=BOTTOM)

        self.play_box = tk.Text(self.r, background="green", width=20, height=10)
        self.play_box.pack(in_=play_frame, side=TOP)
        self.play_button = tk.Button(self.r, text='Play', width=25, command=self.on_play)
        self.play_button.pack(in_=play_frame, side=BOTTOM)

    def set_recording(self, on: bool):
        self.rec_box.config(background="blue" if on else "green")
        self.rec_button.config(text="Recording" if on else "Record")

    def set_playback(self, on: bool):
        self.play_box.config(background="blue" if on else "green")
        self.play_button.config(text="Playing" if on else "Play")

    def start_rec_timer(self, ms: int, cb: Callable[[], None]):
        self.rec_timer = self.r.after(ms, cb)

    def cancel_rec_timer(self):
        if self.rec_timer:
            self.r.after_cancel(self.rec_timer)
            self.rec_timer = None

    def start_playback_timer(self, ms: int, cb: Callable[[], None]):
        self.play_timer = self.r.after(ms, cb)

    def cancel_playback_timer(self):
        if self.play_timer:
            self.r.after_cancel(self.play_timer)
            self.play_timer = None

    def run(self):
        self.r.mainloop()
