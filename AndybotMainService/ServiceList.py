from HelpUtil.Gui import Gui
from Services.Toss import Toss
from Services.News import News
from Services.Fortune import Fortune
from Services.Calendar import Calendar
from HelpUtil.DateTime import Datetime as dt
from time import sleep
from HelpUtil.Kakao import KakaoTalk


class AndyBot:
    def __init__(self, version: str, mode: bool = True):
        self.release = mode
        self.kakao_coc = "COC리코대"
        self.kakao_sso = "SSO/EAM/IM"
        self.version: str = version
        self.date_init = dt.datetime_control()
        self.str_toss = ""
        self.toss("", 1)
        print("ANDY [BOT Initialized] ..........done\nversion : " + self.version)
        print("본 프로그램은 23:00 ~ 익일 02:10 사이는 서비스가 불가합니다.")
        print("본 프로그램은 수정, 테스트, 코드리뷰 환영합니다. 상업적 용도로는 사용하지 말아주세요.")
        print('made by 앤디황')

    def toss(self, chatroom_name: str, count: int = 30):
        if count < 1:
            print('\n' + dt.datetime_control(
                '%Y-%m-%d %H:%M:%S') + ' : toss End, recently update time : ' + str(self.date_init))
            return 0
        try:
            obj = Toss(self.date_init, self.str_toss)
            self.date_init = obj.date_init
            self.str_toss = obj.str_toss
            if chatroom_name == '' and self.release:
                obj.print()
                return 0
            KakaoTalk.send(chatroom_name, "▶ 앤디[봇] 토스 행운퀴즈 Ver " + self.version + " ◀\n\n" + obj.str_toss, self.release)
            raise
        except Exception as e:
            if chatroom_name != '':
                sleep(10)
            count -= 1
            return self.toss(chatroom_name, count)

    def news(self, chatroom_name: str, count: int = 6):
        if count < 1:
            print('\n' + dt.datetime_control(
                '%Y-%m-%d %H:%M:%S') + ' : [' + chatroom_name + '] news End')
            return 0
        try:
            if count > 3:
                news = News.quick_news()
            else:
                news = News.lee_news()
            KakaoTalk.send(chatroom_name, "▶ 앤디[봇] 오늘의 뉴스 Ver " + self.version + " ◀\n" + news, self.release)

        except Exception as e:
            print(e)
            sleep(600)
            count -= 1
            return self.news(chatroom_name, count)

    def fortune(self, chatroom_name: str, count: int = 3):
        if count < 1:
            print('\n' + dt.datetime_control(
                '%Y-%m-%d %H:%M:%S') + ' : [' + chatroom_name + '] fortune End')
            return 0
        try:
            KakaoTalk.send(chatroom_name, "▶ 앤디[봇] " + dt.datetime_control('년 월 일') + " 띠별 운세 Ver " + self.version
                           + " ◀\n\n" + Fortune.bnt_news(), self.release)
        except Exception as e:
            print(e)
            sleep(600)
            count -= 1
            return self.fortune(chatroom_name, count)

    def personal_fortune(self, chatroom_name: str, count: int = 3):
        if count < 1:
            print('\n' + dt.datetime_control(
                '%Y-%m-%d %H:%M:%S') + ' : [' + chatroom_name + '] fortune End')
            return 0
        try:
            KakaoTalk.send(chatroom_name, "▶ 앤디[봇] " + dt.datetime_control('년 월 일') + " 개별 운세 Ver " + self.version
                           + " ◀\n\n" + Fortune.write(), self.release)
        except Exception as e:
            print(e)
            sleep(600)
            count -= 1
            return self.personal_fortune(chatroom_name, count)

    def calendar(self, chatroom_name: str, count: int = 3):
        if count < 1:
            print('\n' + dt.datetime_control(
                '%Y-%m-%d %H:%M:%S') + ' : [' + chatroom_name + '] calendar could not Send')
            return 0
        try:
            obj = Calendar('서울특별시 영등포구 여의동', '영등포구')
            KakaoTalk.send(chatroom_name, "▶ 앤디[봇] 오늘의 일정 Ver " + self.version + " ◀\n\n" + obj.write(), self.release)
        except Exception as e:
            print(e)
            sleep(60)
            count -= 1
            return self.calendar(chatroom_name, count)

    def boot(self):
        _make = Gui(self)
        _make.create()
