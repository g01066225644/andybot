from VariableData import Requests
from VariableData import Datetime as dt
from VariableData import DayControl as dc
import xmltodict


class DataGo:
    def __init__(self):
        self._api_key = 'l3i6oyfhyEYniVFrkI6NMw7INERoMDfZf9L4wVAqARS/C1OZuo3FCmY8rmX8ksBVr/zlyYayhBm3qbFBzhZecw=='
        self._dust_url = 'http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty'
        self._weather_url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'
        self._holiday_url = 'http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getRestDeInfo'
        self._holiday = self.get_holiday_list()
        self._sky1 = 0
        self._sky2 = 0
        self._temp = 0
        self._rain = 0
        self._mint = 0
        self._maxt = 0
        self._time = ''
        self._pm10 = ''
        self._pm25 = ''
        self._khai = ''

    @property
    def temperature(self):
        return self._temp

    @temperature.setter
    def temperature(self, value):
        self._temp = value

    @property
    def rain(self):
        return self._rain

    @rain.setter
    def rain(self, value):
        self._rain = value

    @property
    def min_temperature(self):
        return self._mint

    @min_temperature.setter
    def min_temperature(self, value):
        self._mint = value

    @property
    def max_temperature(self):
        return self._maxt

    @max_temperature.setter
    def max_temperature(self, value):
        self._maxt = value

    @property
    def measure_time(self):
        return self._time

    @measure_time.setter
    def measure_time(self, value):
        self._time = value

    @property
    def pm10(self):
        return self._pm10

    @pm10.setter
    def pm10(self, value):
        self._pm10 = value

    @property
    def pm25(self):
        return self._pm25

    @pm25.setter
    def pm25(self, value):
        self._pm25 = value

    @property
    def khai(self):
        return self._khai

    @khai.setter
    def khai(self, value):
        self._khai = value

    @staticmethod
    def request_to_data_go_kr(url: str, params: dict) -> dict | bool:
        response = Requests.session(url, params=params)
        xml_data = response.text
        dict_data = xmltodict.parse(xml_data)
        if "SERVICE ERROR" in str(dict_data):
            return False
        elif dict_data['response']['header']['resultCode'] != '00':
            print(dt.datetime_control('%Y-%m-%d %H:%M:%S') + ' : ' + url + str(params) + '\nErrorMsg : ' + dict_data['response']['header']['resultMsg'])
            return False
        else:
            return dict_data['response']['body']['items']['item']

    def get_holiday_list(self, value=dt.datetime_control().today()):
        params = {
            "ServiceKey": self._api_key,
            "solYear": value.year,
            "numOfRows": 100
        }
        holiday_list = []
        for item in DataGo.request_to_data_go_kr(self._holiday_url, params):
            item_dict = {
                'name': item["dateName"],
                'date': dt.strptime(item["locdate"], '%Y%m%d')
            }
            holiday_list.append(item_dict)
        return holiday_list

    # 오늘이 과연 공휴일인가....
    def is_holiday(self, value=dt.datetime_control()):
        if len(self._holiday) == 0:
            return ''
        for item in self._holiday:
            if value.date() == item['date'].date():
                return item['name']
            else:
                continue
        return ''

    # 공휴일, 주말 제외 평일
    def get_week_day(self, value):
        if value.weekday() >= 5 or self.is_holiday(value) != '':
            return self.get_week_day(value - dc(1))
        else:
            return value.date()

    @staticmethod
    def get_forecast_time(now_time=dt.datetime_control()):
        # 다음 정각 기준 예보
        hour = now_time.hour + 1
        if hour < 10:
            return '0' + str(hour) + '00'
        else:
            return str(hour) + '00'

    def parsing_sky(self):
        sky_parser = {
            0: '',
            1: '청명함',
            2: '대체로 청명함',
            3: '대체로 흐림',
            4: '흐림',
            5: '비 (가수 비 아님ㅎ)',
            6: '진눈깨비',
            7: '눈',
            8: '소나기',
        }
        if self._sky1 == self._sky2:
            return sky_parser.get(self._sky1)
        elif self._sky1 == 0 or self._sky2 == 0:
            return sky_parser.get(self._sky1 + self._sky2)
        else:
            return '오전엔 ' + sky_parser.get(self._sky1) + ', ' + '오후엔 ' + sky_parser.get(self._sky2)

    def weather_code(self, key, value, ftime):
        now_time = DataGo.get_forecast_time()
        afternoon = '1500'
        if int(now_time) > int(afternoon):
            afternoon = ''
        match key:
            # 1시간 기온
            case 'TMP':
                if ftime == now_time:
                    self.temperature = value
            # 강수확률
            case 'POP':
                if ftime == now_time:
                    self.rain = value
            # 하늘상태 청명함(1) 구름많은(3) 흐림(4)
            case 'SKY':
                if ftime == now_time:
                    self._sky1 = int(value)
                elif ftime == afternoon:
                    self._sky2 = int(value)
            # 강수형태 없음(0), 비(1), 진눈깨비(2), 눈(3), 소나기(4)
            case 'PTY':
                if ftime == now_time:
                    self._sky1 += int(value)
                elif ftime == afternoon:
                    self._sky2 += int(value)
            # 일 최고기온
            case 'TMX':
                self.max_temperature = value
            # 일 최저기온
            case 'TMN':
                self.min_temperature = value

    def get_weather_forecast(self, nx, ny):
        params = {
            'ServiceKey': self._api_key,
            'base_date': dt.datetime_control('%Y%m%d'),
            'base_time': '0200',
            'nx': nx,
            'ny': ny,
            'pageNo': 1,
            'numOfRows': 1000,
            'dataType': 'XML'
        }
        data = DataGo.request_to_data_go_kr(self._weather_url, params)
        if data:
            for item in data:
                if item['fcstDate'] == params.get('base_date'):
                    self.weather_code(item['category'], item['fcstValue'], item['fcstTime'])
            return True
        else:
            return False

    def get_air_quality(self, obs_name: str):
        params = {
            'stationName': obs_name,
            'dataTerm': 'DAILY',
            'ver': '1.3',
            'serviceKey': self._api_key,
            'returnType': 'xml',
            'numOfRows': 1
        }
        grade_parser = {
            '1': "좋음",
            '2': "보통",
            '3': "나쁨",
            '4': "매우 나쁨",
            None: "측정 오류"
        }
        data = DataGo.request_to_data_go_kr(self._dust_url, params)
        if data:
            for key, value in data.items():
                match key:
                    case 'dataTime':
                        self.measure_time = value
                    case 'pm10Grade1h':
                        self.pm10 = grade_parser.get(value)
                    case 'pm25Grade1h':
                        self.pm25 = grade_parser.get(value)
                    case 'khaiGrade':
                        self.khai = grade_parser.get(value)
            return True
        else:
            return False
