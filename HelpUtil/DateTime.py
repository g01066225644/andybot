from HelpUtil import datetime, timedelta
from pytz import timezone
from korean_lunar_calendar import KoreanLunarCalendar


class Datetime(datetime):

    def __new__(cls, *args, **kwargs):
        dt_obj = super().__new__(cls, *args, **kwargs)
        return dt_obj

    # 테스트 용도 외에는 절대루 호출하지 않는다.
    @classmethod
    def __force__(cls, *args):
        cls.fixed = cls(*args)

    @classmethod
    def is_fixed(cls):
        if hasattr(cls, 'fixed'):
            return True
        else:
            return False

    # datetime.now() 대신
    @classmethod
    def now(cls, tz=None):
        if hasattr(cls, 'fixed'):
            return cls.fixed
        return super().now(timezone("Asia/Seoul"))

    @classmethod
    def lunar_datetime(cls, that_day: datetime) -> datetime:
        calendar1 = KoreanLunarCalendar()
        calendar1.setLunarDate(that_day.year, that_day.month, that_day.day, False)
        # 생일이 겁내 느림
        if datetime.strptime(calendar1.SolarIsoFormat(), '%Y-%m-%d').year > datetime.today().year:
            calendar2 = KoreanLunarCalendar()
            calendar2.setLunarDate(datetime.today().year - 1, that_day.month, that_day.day, False)
            return datetime.strptime(
                calendar2.SolarIsoFormat(), '%Y-%m-%d')
        else:
            return datetime.strptime(
                calendar1.SolarIsoFormat(), '%Y-%m-%d')

    @classmethod
    def lunar_datetime_control(cls, is_check_year: bool, *args) -> datetime:
        that_day = cls(*args)
        if is_check_year:
            return cls.lunar_datetime(that_day)
        else:
            now_day = that_day.replace(year=Datetime.datetime_control().year)
            return cls.lunar_datetime(now_day)

    @classmethod
    def times_of_weekday(cls, times: int, _weekday: int, *args) -> datetime:
        today: datetime = cls.datetime_control(*args)
        first_day_of_month = today.replace(day=1)  # 이번 달의 첫째 날
        return first_day_of_month + timedelta((_weekday - first_day_of_month.weekday() + 7) % 7) + timedelta(
            (times - 1) * 7)

    @classmethod
    def next_weekday(cls) -> datetime:
        today = cls.datetime_control()
        current_day_of_week = today.weekday()
        return today + timedelta(7 - current_day_of_week)

    @classmethod
    def datetime_control(cls, date_format: str = None, *args):
        that_time = Datetime.now(timezone("Asia/Seoul"))
        if args:
            if isinstance(args[0], datetime):
                that_time = args[0]
            elif isinstance(args, tuple):
                that_time = cls(*args)

        weekday_parser = {0: '월', 1: '화', 2: '수', 3: '목', 4: '금', 5: '토', 6: '일'}
        match date_format:
            case None:
                return that_time
            case '일':
                return str(that_time.day) + '일'
            case '월 일':
                return str(that_time.month) + '월 ' + str(that_time.day) + '일'
            case '월 일 요일':
                return str(that_time.month) + '월 ' + str(that_time.day) + '일 ' + str(
                    weekday_parser.get(that_time.weekday())) + '요일'
            case '년 월 일':
                return str(that_time.year) + '년 ' + str(that_time.month) + '월 ' + str(that_time.day) + '일'
            case '년 월 일 요일 시 분':
                return (str(that_time.year) + '년 ' + str(that_time.month) + '월 ' + str(that_time.day) + '일 ' + str(
                    weekday_parser.get(that_time.weekday())) + '요일 ' + str(that_time.hour) + '시 ' + str(
                    that_time.minute) + '분')
            case '월일':
                return str(that_time.month) + '월' + str(that_time.day) + '일'
            case '년월일':
                return str(that_time.year) + '년' + str(that_time.month) + '월' + str(that_time.day) + '일'
            case _:
                return that_time.strftime(date_format)

    @staticmethod
    def trans_string_to_date(text) -> datetime:
        current_time = Datetime.datetime_control()
        index_month = text.find('월')
        if index_month != -1:
            month = text[index_month - 2:index_month]
        else:
            month = current_time.month
        index_day = text.find('일')
        if index_day != -1:
            day = text[index_day - 2:index_day]
        else:
            day = current_time.day

        return datetime(current_time.year, int(month), int(day), current_time.hour, current_time.minute,
                        current_time.second)


class DayControl(timedelta):

    def __new__(cls, *args, **kwargs):
        dt_obj = super().__new__(cls, *args, **kwargs)
        return dt_obj
