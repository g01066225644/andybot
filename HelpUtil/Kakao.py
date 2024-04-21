from HelpUtil import sleep
#import win32api
#import win32con
#import win32gui


class KakaoTalk:

    @staticmethod
    def send(kakao_chatroom, message, is_release):
        if is_release:
            obj = KakaoTalk()
            obj.open_chatroom(kakao_chatroom)
            obj.kakao_sendtext(kakao_chatroom, message)
        else:
            print(message)

    # # 채팅방에 메시지 전송
    def kakao_sendtext(self, chatroom_name, message):
        # # 핸들 _ 채팅방
        hwnd_main = win32gui.FindWindow(None, chatroom_name)
        hwnd_edit = win32gui.FindWindowEx(hwnd_main, None, "RICHEDIT50W", None)
        win32api.SendMessage(hwnd_edit, win32con.WM_SETTEXT, 0, message)
        self.send_return(hwnd_edit)

    # # 엔터
    def send_return(self, hwnd):
        win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
        sleep(0.01)
        win32api.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_RETURN, 0)

    # # 채팅방 열기
    # # # 채팅방 목록 검색하는 Edit (채팅방이 열려있지 않아도 전송 가능하기 위하여)
    def open_chatroom(self, kakao_chatroom):
        hwndkakao = win32gui.FindWindow(None, "카카오톡")
        hwndkakao_edit1 = win32gui.FindWindowEx(hwndkakao, None, "EVA_ChildWindow", None)
        hwndkakao_edit2_1 = win32gui.FindWindowEx(hwndkakao_edit1, None, "EVA_Window", None)
        hwndkakao_edit2_2 = win32gui.FindWindowEx(hwndkakao_edit1, hwndkakao_edit2_1, "EVA_Window", None)
        hwndkakao_edit3 = win32gui.FindWindowEx(hwndkakao_edit2_2, None, "Edit", None)
        # # Edit에 검색 _ 입력되어있는 텍스트가 있어도 덮어쓰기됨
        win32api.SendMessage(hwndkakao_edit3, win32con.WM_SETTEXT, 0, kakao_chatroom)
        sleep(1)  # 안정성 위해 필요
        self.send_return(hwndkakao_edit3)
        sleep(1)
