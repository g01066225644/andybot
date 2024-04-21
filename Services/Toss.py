from Services import Requests
from Services import Datetime as dt
from Services import BeautifulSoup


class Toss:
    def __init__(self, date_init, str_toss):
        self._date_init = date_init
        self._str_toss = str_toss
        self.bnt_news()

    @property
    def date_init(self):
        return self._date_init

    @date_init.setter
    def date_init(self, init):
        self._date_init = init

    @property
    def str_toss(self):
        return self._str_toss

    @str_toss.setter
    def str_toss(self, toss_answer):
        self._str_toss = toss_answer

    def print(self):
        index = self.str_toss.find('\n\n')
        if index == -1:
            index = len(self.str_toss)
        print("토스퀴즈 최근 정답 : \n" + self.str_toss[:index])
        print("토스퀴즈 최근 날짜 : " + str(self.date_init.date()))
        print(dt.datetime_control(
            '%Y-%m-%d %H:%M:%S') + ' : 최근 정답, 날짜 이상 없는지 확인하고 [시작] 잘못 가져왔으면 [재시작]으로 다시 실행한다.')

    def bnt_news(self):
        search = "https://www.bntnews.co.kr/article/search?searchText=토스+행운퀴즈"
        response = Requests.session(search)
        soup = BeautifulSoup(response.text, 'html.parser')
        at = soup.select_one('#list > article:nth-child(1) > a')['href']
        child_response = Requests.session("https://www.bntnews.co.kr" + at)
        child_soup = BeautifulSoup(child_response.text, 'html.parser')
        nindex = child_soup.text.find('■')
        today = dt.datetime_control('월 일')
        if (today in child_soup.text[:nindex] and self.date_init.date() <= dt.trans_string_to_date(
                child_soup.text).date()) or self.str_toss == '':
            contents = child_soup.select_one(
                '#wrap_index > main > div > div:nth-child(1) > div > div.din.din2-12.view_din > div:nth-child(2) > div.box.body_wrap > div.content')
            selected = contents.select('strong')
            if ('▶' not in selected[0].text and selected[1].text[7:] not in self.str_toss) or self.str_toss == '':
                toss_list = []
                for asp in selected:
                    if not asp.text.startswith('▶'):
                        toss_list.append("\n")
                    toss_list.append(asp.text)
                self.str_toss = '\n'.join(toss_list[1:])
                self.date_init = dt.trans_string_to_date(child_soup.text[:nindex])
            else:
                raise Exception(dt.datetime_control('%Y-%m-%d %H:%M:%S') + ' : toss answer has not provided yet')
        else:
            raise Exception(dt.datetime_control('%Y-%m-%d %H:%M:%S') + ' : toss get Wrong date [' + str(
                dt.trans_string_to_date(child_soup.text)) + ']')
