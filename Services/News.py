from Services import Requests
from Services import Datetime as dt
from Services import BeautifulSoup


class News:

    @staticmethod
    def quick_news():
        response = Requests.session("https://quicknews.co.kr/?day=before")
        soup = BeautifulSoup(response.text, 'html.parser')
        at = soup.select_one('#news_0')
        if dt.datetime_control('%Y-%m-%d') in at.nextSibling:
            return at.text
        else:
            raise Exception(dt.datetime_control('%Y-%m-%d %H:%M:%S') + ' : quick_news has not uploaded yet')

    @staticmethod
    def lee_news():
        response = Requests.session(
            "https://blog.naver.com/PostList.nhn?blogId=totcar&widgetTypeCall=true&categoryNo=1&directAccess=true")
        soup = BeautifulSoup(response.text, 'html.parser')
        child_uri = soup.select_one('#PostThumbnailAlbumViewArea > ul > li > a')['href']  # 첫번째 게시글
        first_nindex = child_uri.find('&logNo=')
        last_nindex = child_uri.find('&categoryNo=')
        post_view_id = '#post-view' + child_uri[first_nindex + 7:last_nindex]
        child_response = Requests.session("https://blog.naver.com" + child_uri)
        child_soup = BeautifulSoup(child_response.text, 'html.parser')
        main_container = child_soup.select_one(post_view_id + '> div > .se-main-container')
        contents = main_container.select(
            '.se-component.se-text.se-l-default > .se-component-content > .se-section.se-section-text.se-l-default > .se-module.se-module-text > p')  # 없을 수도 있음
        if len(contents) != 0:
            if dt.datetime_control('월 일') in contents[0].text:
                news = []
                for content in contents:
                    news.append(content.text)
                output = '\n'.join(news)
                return output
            else:
                raise Exception(
                    dt.datetime_control('%Y-%m-%d %H:%M:%S') + ' : LeeSecheol_news has not uploaded yet')
        else:
            raise Exception(
                dt.datetime_control('%Y-%m-%d %H:%M:%S') + ' : LeeSecheol_news has no contents')

    def write(self):
        return self.lee_news() + '\n\n\n' + self.quick_news()
