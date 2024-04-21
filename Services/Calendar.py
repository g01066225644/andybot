from Services import Datetime as dt
from VariableData.RequestToApi import DataGo
from VariableData.Raon import SSORND
from VariableData.Grid import Grid


class Calendar:
    def __init__(self, location='서울특별시 영등포구 여의동', obs_name='영등포구'):
        self.data = None
        xy = Grid(location)
        self.nx = xy.get_xy()[0]
        self.ny = xy.get_xy()[1]
        self._obs_name = obs_name
        self._comment = ''

    # 계정관리개발팀
    def get_raon_calendar(self, value) -> str:

        sso = SSORND()
        dolist = []
        cal = []
        for key, values in sso.get_birthday(False).items():
            if value.month == key.month and value.day == key.day:
                cal.append(str(sso.get_birthday(False)[key]) + ' 생일')
        if self.data.is_holiday(value) != '':
            cal.append(self.data.is_holiday(value))
        if value.date() == sso.get_salary_day():
            cal.append('월급날')
        if value.date() == sso.get_family_day():
            cal.append('패밀리데이')
        if value.date() == sso.get_deadline_tax_exemption():
            cal.append('개인경비 지출결의서 결재 마감일')
        if sso.is_etc_do(value):
            cal.append(sso.is_etc_do(value))

        if sso.is_fooding(value):
            dolist.append('푸딩')
        if sso.is_report(value):
            dolist.append('주간보고')

        str_cal = '오늘은 ' + ', '.join(map(str, cal)) + '입니다.\n\n'
        str_dolist = '오늘 할일은 ' + ', '.join(map(str, dolist)) + '해야 합니다.\n\n'
        if len(cal) == 0:
            str_cal = '오늘의 일정은 없습니다.\n\n'
        if len(dolist) != 0:
            str_cal += str_dolist
        if sso.is_fooding(value):
            str_cal += sso.get_fooding()
        return str_cal

    def is_rainy(self):
        if '비' in self.data.parsing_sky() or '눈' in self.data.parsing_sky() or '소나기' in self.data.parsing_sky():
            return "우산을 챙기는 것이 좋겠네요.\n"
        else:
            return ''

    def which_clothes(self):
        if float(self.data.max_temperature) >= 28:
            return "매우 덥습니다. 민소매, 반팔, 반바지 등 시원한 옷을 입으세요.\n\n"
        elif float(self.data.max_temperature) >= 23:
            return "좀 덥습니다. 반팔, 얇은 셔츠, 반바지 얇은 긴바지 등을 입으세요.\n\n"
        elif float(self.data.max_temperature) >= 20:
            return "활동하기 좋은 날씨 입니다. 긴팔 티, 긴바지는 어떠세요?\n다만, 일교차를 대비해 얇은 아우터를 챙기는 것이 좋습니다.\n\n"
        elif float(self.data.max_temperature) >= 12:
            return "쌀쌀한 날씨입니다. 자켓에 셔츠, 니트, 가디건, 후드티는 어떠세요?\n저녁엔 아우터를 챙기세요.\n\n"
        elif float(self.data.max_temperature) >= 9:
            return "좀 춥겠네요. 트렌치코트, 후리스, 두툼한 자켓을 입어야 합니다.\n다만, 내의를 입을 날씨는 아닙니다.\n\n"
        elif float(self.data.max_temperature) >= 5:
            return "춥습니다. 코트, 가죽 자켓, 패딩 등을 입으세요.\n추위를 탄다면 내의를 입으세요.\n\n"
        elif float(self.data.max_temperature) < 5:
            return "한겨울 날씨입니다. 두꺼운 코트, 롱패딩, 두꺼운 니트, 기모 제품을 입으세요.\n\n"

    def air_quality(self):
        if '좋음' in self.data.khai:
            return "대기질이 깨끗하니, 신선한 공기를 마셔보세요.\n\n"
        elif '보통' in self.data.khai:
            return "환기는 조금만 하고, 외출할 때는 호흡기 건강에 신경쓰세요.\n\n"
        elif '나쁨' in self.data.khai:
            return "호흡기 건강이 좋지 않다면, 외출을 삼가세요.\n\n"
        else:
            return ''

    def write(self):
        self.data = DataGo()
        comment = ("안녕하세요\n"
                   "지금은 {}입니다.\n").format(dt.datetime_control('년 월 일 요일 시 분'))
        if self.data.get_weather_forecast(self.nx, self.ny):
            comment += ("오늘의 날씨는 {}입니다.\n"
                       "현재 체감온도는 {}ºC, 강수 확률은 {}%입니다.\n").format(
                self.data.parsing_sky(), self.data.temperature, self.data.rain)
            comment += self.is_rainy()
            comment += "최고기온은 {}ºC, 최저기온은 {}ºC입니다.\n" \
                .format(self.data.max_temperature, self.data.min_temperature)
            comment += self.which_clothes()
        if self.data.get_air_quality(self._obs_name):
            comment += ("대기질 상태입니다.\n"
                        "미세먼지 : {}, 초미세먼지 : {},\n통합대기 지수 : {}입니다.\n").format(
                self.data.pm10, self.data.pm25, self.data.khai)
            comment += self.air_quality()

        comment += self.get_raon_calendar(dt.datetime_control())
        comment += "오늘도 좋은 하루 되세요.\n\n출처. 기상청, {}청\n{} 기준.".format(self._obs_name, self.data.measure_time)
        return comment
