from VariableData import Datetime as dt
from VariableData import DayControl as dc
from VariableData.RequestToApi import DataGo
from VariableData import Read


class SSORND:
    def __init__(self):
        self.that_day = DataGo()
        self.year = dt.datetime_control().year
        self.month = dt.datetime_control().month

    @staticmethod
    def get_birthday(check: bool):
        dict_birth = {
            dt.lunar_datetime_control(check, 1979, 8, 20): "박수희 팀장님",
            dt.datetime_control(None, 1980, 5, 31): "왕현정 프로님",
            dt.datetime_control(None, 1981, 6, 11): "김승모 프로님",
            dt.datetime_control(None, 1980, 6, 8): "안한진 프로님",
            dt.datetime_control(None, 1981, 4, 12): "전규철 프로님",
            dt.lunar_datetime_control(check, 1981, 11, 25): "심원종 프로님",
            dt.datetime_control(None, 1983, 3, 28): "조우문 프로님",
            dt.datetime_control(None, 1988, 1, 11): "진수준 프로님",
            dt.datetime_control(None, 1995, 4, 10, 15, 37, 0): "앤디황 프로님",
            dt.datetime_control(None, 1988, 10, 22): "오지수 프로님",
            dt.datetime_control(None, 1996, 1, 10): "전효정 프로님",
            dt.datetime_control(None, 1993, 6, 16): "원지연 프로님",
            dt.datetime_control(None, 1998, 5, 18): "안현서 사원님",
            dt.datetime_control(None, 2012, 10, 2): "라온"
        }
        return dict_birth

    @staticmethod
    def get_floor_clean(self):
        floor_list = []
        return floor_list

    def get_salary_day(self):
        return self.that_day.get_week_day(dt(self.year, self.month, 10))

    @staticmethod
    def get_family_day():
        return dt.times_of_weekday(3, 4).date()

    def get_deadline_tax_exemption(self):
        return self.that_day.get_week_day(dt(self.year, self.month, 5))

    def is_fooding(self, value: dt) -> bool:
        if value.weekday() == 2:
            return True
        else:
            return False

    def get_fooding(self) -> str:
        comment = '\n다음 주 푸딩 주소\n'
        next_week = dt.next_weekday()
        for i in range(5):
            holiday = self.that_day.is_holiday(next_week + dc(i))
            comment += dt.datetime_control('월 일 요일', next_week + dc(i)) + " : "
            if holiday == '':
                comment += "https://app.fooding.io/daily-menus?date=" + (next_week + dc(i)).strftime(
                    "%Y%m%d") + "&serviceTime=1\n\n"
            else:
                comment += holiday + '\n\n'
        return comment

    def is_report(self, value: dt) -> bool:
        if value.weekday() == 3:
            return True
        else:
            return False

    def is_etc_do(self, value: dt) -> str:
        do_list = []
        caritas = Read('caritas.csv')
        floorclean = Read('floorclean.csv')

        for key, values in caritas.get_data().items():
            if value.date() == key.date():
                do_list.append(values + ' 까리따스 가는 날ㅋ ')
        for key, values in floorclean.get_data().items():
            if value.date() == key.date():
                do_list.append(values)

        return ', '.join(map(str, do_list))

