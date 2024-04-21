import ast
from Services import Requests
from Services import Datetime as dt
from Services import BeautifulSoup
from VariableData.Raon import SSORND


class Fortune:
    @staticmethod
    def aju_news():
        url = ("https://www.ajunews.com/search?q=%EB%9D%A0%EB%B3%84%20%EC%9A%B4%EC%84%B8&sdate="
               + dt.datetime_control('%Y.%m.%d') + "&edate=" + dt.datetime_control('%Y.%m.%d') + "&dateview=1&search_gubun=A")
        response = Requests.session(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        if '요청하신 검색어에 대한 검색결과가 없습니다.' not in soup.select_one('#container > div > article > div > section.article_wrap.left_content').text:
            today_url = soup.select_one('#container > div > article > div > section.article_wrap.left_content > ul > li > div > a.tit')['href']
            child_response = Requests.session('https:' + today_url)
            child_soup = BeautifulSoup(child_response.text, 'html.parser')
            fortune_str = child_soup.select_one('#articleBody > div:nth-child(2)')
            return fortune_str.text
        else:
            raise Exception(dt.datetime_control('%Y-%m-%d %H:%M:%S') + ' : aju_news has not uploaded yet')

    @staticmethod
    def bnt_news():
        search = "https://www.bntnews.co.kr/article/search?searchText=%EB%9D%A0%EB%B3%84+%EC%9A%B4%EC%84%B8"
        response = Requests.session(search)
        soup = BeautifulSoup(response.text, 'html.parser')
        at = soup.select_one('#list > article:nth-child(1) > a')['href']
        child_response = Requests.session("https://www.bntnews.co.kr" + at)
        child_soup = BeautifulSoup(child_response.text, 'html.parser')
        nindex = child_soup.text.find('bnt뉴스')
        today = dt.datetime_control('월 일')
        if today in child_soup.text[:nindex]:
            contents = child_soup.select_one('#wrap_index > main > div > div:nth-child(1) > div > div.din.din2-12.view_din > div:nth-child(2) > div.box.body_wrap > div.content')
            br_tags = contents.find_all('br')

            # Replace each <br> tag with '\n'
            for br_tag in br_tags:
                br_tag.replace_with('\n')

            selected = contents.text.replace('\n\n\n\n\n\n\n', '\n\n')
            start = selected.find('[ 쥐띠 ]')
            end = selected.find('오늘띠별운세')
            return selected[start:end]
        else:
            raise

    @staticmethod
    def raon_sso(value: dt) -> str:
        str_data = ''
        gender = 'm'
        if (value.date() == dt.datetime_control(None, 1980, 5, 31).date()
                or value.date() == dt.datetime_control(None, 1988, 10, 22).date()
                or value.date() == dt.datetime_control(None, 1996, 1, 10).date()
                or value.date() == dt.datetime_control(None, 1993, 6, 16).date()
                or value.date() == dt.datetime_control(None, 1998, 5, 18).date()):
            gender = 'f'
        url = (("https://search.naver.com/p/csearch/dcontent/external_api/json_todayunse_v2.naver?_callback=window"
                ".__jindo2_callback._fortune_my_0&gender=" + gender + "&birth=")
               + dt.datetime_control('%Y%m%d', value)
               + "&solarCal=solar&time=")
        response = Requests.session(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        start = soup.text.find('[')
        end = soup.text.find(']')
        data = ast.literal_eval(soup.text[start:end + 1])
        for datum in data:
            if 'keyword' in datum:
                str_data += datum['keyword'] + '\n'
            elif datum['name'] == '행운사항':
                continue
            elif 'name' in datum:
                str_data += '\n' + datum['name'] + '\n'
            str_data += datum['desc']
        return SSORND.get_birthday(True).get(value) + ' :\n' + str_data + '\n\n'

    @staticmethod
    def write() -> str:
        luck = ''
        keys = SSORND.get_birthday(True).keys()
        for key in keys:
            luck += Fortune.raon_sso(key)
        return luck

