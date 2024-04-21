import os
import sys
import tkinter
from HelpUtil.Schedule import SchedulerThread


class Gui:
    def __init__(self, app_instance):
        self.scheduler_thread = None
        self.start_button = None
        self.pause_button = None
        self.resume_button = None
        self.exit_button = None
        self.app_instance = app_instance

    def start(self):
        self.start_button.config(state=tkinter.DISABLED)
        self.pause_button.config(state=tkinter.NORMAL)
        self.resume_button.config(state=tkinter.NORMAL)
        if self.scheduler_thread:
            self.scheduler_thread.resume()
        else:
            self.scheduler_thread = SchedulerThread(self.app_instance)
            self.scheduler_thread.daemon = True
            self.scheduler_thread.start()

    def pause(self):
        self.start_button.config(state=tkinter.NORMAL)
        self.pause_button.config(state=tkinter.DISABLED)
        if self.scheduler_thread:
            self.scheduler_thread.pause()

    def restart(self):
        self.pause_button.config(state=tkinter.NORMAL)
        python = sys.executable
        os.execl(python, python, *sys.argv)

    def create(self):
        window = tkinter.Tk()
        window.title("앤디봇")
        window.geometry("400x100")
        window.resizable(False, False)
        self.start_button = tkinter.Button(window, text="시작", command=self.start)
        self.start_button.pack(side=tkinter.LEFT, padx=5, pady=5, fill=tkinter.BOTH, expand=True)

        self.pause_button = tkinter.Button(window, text="일시정지", command=self.pause, state=tkinter.DISABLED)
        self.pause_button.pack(side=tkinter.LEFT, padx=5, pady=5, fill=tkinter.BOTH, expand=True)

        self.resume_button = tkinter.Button(window, text="재시작", command=self.restart)
        self.resume_button.pack(side=tkinter.LEFT, padx=5, pady=5, fill=tkinter.BOTH, expand=True)

        self.exit_button = tkinter.Button(window, text="종료", command=window.destroy)
        self.exit_button.pack(side=tkinter.LEFT, padx=5, pady=5, fill=tkinter.BOTH, expand=True)

        window.mainloop()
