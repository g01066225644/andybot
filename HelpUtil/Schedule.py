import threading
import schedule
from itertools import cycle
from HelpUtil import sleep
from HelpUtil.DateTime import Datetime as dt


class SchedulerThread(threading.Thread):
    def scheduled_job(self):
        schedule.every().day.at('06:50').do(self.make_thread, self.app.calendar, self.app.kakao_sso, 3)
        schedule.every().day.at('08:00').do(self.make_thread, self.app.news, self.app.kakao_sso, 6)
        schedule.every().day.at('08:01').do(self.make_thread, self.app.news, self.app.kakao_coc, 6)
        schedule.every().day.at('09:00').do(self.make_thread, self.app.personal_fortune, self.app.kakao_sso, 3)
        schedule.every().day.at('09:01').do(self.make_thread, self.app.fortune, self.app.kakao_coc, 3)
        schedule.every().hour.at(':00').do(self.make_thread, self.app.toss, self.app.kakao_sso, 30)

    def __init__(self, app_instance):
        super().__init__()
        self.app = app_instance
        self.paused = False
        self.terminate = False

    @staticmethod
    def make_thread(function, chatroom: str, count: int = 6):
        print('\n' + dt.datetime_control('%Y-%m-%d %H:%M:%S') + ' : ' + str(function) + ' start')
        child_thread = threading.Thread(target=function, args=(chatroom, count))
        child_thread.daemon = True
        child_thread.start()

    def run(self):
        message = 'ANDY [BOT START] '
        pers = cycle(['-', '\\', '|', '/'])
        self.scheduled_job()
        while not self.terminate:
            if not self.paused:
                print('\r' + message + next(pers), end='', flush=True)
                schedule.run_pending()  # 스케줄 실행
            sleep(1)

    def pause(self):
        self.paused = True
        print('\rANDY [BOT PAUSE]', end='', flush=True)

    def resume(self):
        self.paused = False