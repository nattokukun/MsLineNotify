# -*- coding: utf-8 -*-
#__/__/__/__/__/__/__/__/__/__/__/__/__/__/__/__/__/__/__/__/__/__/__/__/__/__/
#
#            kivy Mas LINE Norify
#            2023-02-17 M.Ida
#
#__/__/__/__/__/__/__/__/__/__/__/__/__/__/__/__/__/__/__/__/__/__/__/__/__/__/

#---------------------------------------------------------------------------------
#                   定数定義
#---------------------------------------------------------------------------------
APP_NAME = 'Mas LINE Notify' + '  Ver.1.2'
MENU_ENABLED = True
CHECK_BOX_DOWN = 'down'
BG_BLUE = [  0,  0, 0.5, 1]
BG_RED  = [0.5,  0,   0, 1]

MSG_MAX = 6     # メッセージ数

#------------------------------------------------------------------------------
#                    インポート
#------------------------------------------------------------------------------
from kivy.app import App
# import kivy
# kivy.require('1.11.0')
from kivy.uix.screenmanager import ScreenManager, Screen
import threading
from kivy.clock import Clock

## from kivy.config import Config
from kivy.uix.widget import Widget
## from kivy.properties import ObjectProperty
## from kivy.lang import Builder

from _userlib import cssys
from _userlib.cssys import debug_log
# OpenGLの調整
cssys.adjust_opengl(3, True)

# 日本語画面調整
from _userlib import csuix
csuix.japanize_screen()
#---------------------------------------------------------------------------------
#                   LINE
#---------------------------------------------------------------------------------
from _userlib.linebot import LINENotifyBot

# LINE 送信
def line_notify(p_access_token,     # アクセストークン
                p_msg):             # メッセージ
                                    # エラーメッセージ '':成功
    """
    if cssys.is_windows:
     # ウインドウズではokとする
        return ''
    """

    t_bot = LINENotifyBot(p_access_token)

    ## t_errmsg = t_bot.send(p_msg, p_sticker_package_id=1, p_sticker_id=13)
    from datetime import datetime
    t_now = datetime.now()
    t_datetime = t_now.strftime('%Y-%m-%d %H:%M:%S')
    p_msg = t_datetime + '\n' + p_msg

    debug_log('line notigy : ' + p_msg)
    t_errmsg = t_bot.send(p_msg)

    return t_errmsg

#---------------------------------------------------------------------------------
#                   先頭画面
#---------------------------------------------------------------------------------
class TopScreen(Screen):
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    #            コンストラクタ
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    def __init__(self, **kwargs):
        super(TopScreen, self).__init__(**kwargs)
        # 日本語フォントは恐らく属性変更はNG
        self.ids.label_msg.text = '[b][i]' + APP_NAME + '[/i][/b]'

        # 初期値設定
        self.ids.msg_check_box_1.state  = CHECK_BOX_DOWN
        self.ids.send_check_box_1.state = CHECK_BOX_DOWN

    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    #                処理実行
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    def button_exec(self):
        t_errmsg = ''

        # メッセージ選択
        if t_errmsg == '':
            t_msg = ''
            for t_idx in range(MSG_MAX):
                if self.ids["msg_check_box_" + str(t_idx+1)].state == CHECK_BOX_DOWN:
                    t_msg = self.ids["msg_label_" + str(t_idx+1)].text
                    break
            if t_msg == '':
                t_errmsg = 'メッセージが未選択です。'

        # 送信先選択
        if t_errmsg == '':
            t_send_name = ''
            for t_idx in range(2):
                if self.ids["send_check_box_" + str(t_idx+1)].state == CHECK_BOX_DOWN:
                    t_send_name = self.ids["send_label_" + str(t_idx+1)].text
                    break
            if t_send_name == '':
                t_errmsg = '送信先が未選択です。'

        self.ids.label_errmsg.text = t_errmsg
        if t_errmsg != '':
            cssys.boo()
            return

        # 画面切替
        self.manager.current = 'busy'
        self.manager.current_screen.send_msg  = t_msg
        self.manager.current_screen.send_name = t_send_name

    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    #                終了
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    def button_quit(self):
        quit()

#---------------------------------------------------------------------------------
#                   終了画面
#---------------------------------------------------------------------------------
class EndScreen(csuix.ScreenCustom):
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    #            コンストラクタ
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    def __init__(self, **kwargs):
        super(EndScreen, self).__init__(**kwargs)
        # super().__init__(**kwargs)
        # self.form_init()

    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    #                処理実行
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    def button_exec(self):
        # 画面切替
        if MENU_ENABLED:
            self.manager.current = 'top'
        else:
            self.manager.current = 'busy'

    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    #                終了
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    def button_quit(self):
        quit()

#------------------------------------------------------------------------------
#                    処理画面
#------------------------------------------------------------------------------
class BusyScreen(Screen):
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    #            コンストラクタ
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)

        self.send_msg  = ''
        self.send_name = ''
        self.end_ok  = False
        self.end_msg = ''
        return

    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    #        画面表示終了で処理実行
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    def on_enter(self, *args):
        # スレッド開始
        t_thread = threading.Thread(target=self.process_exec)
        t_thread.start()
        return

    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    #        スレッドにて処理実行
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    def process_exec(self):
        cssys.debug_log('process_exec ' + self.send_msg)

        # to 美枝子
        ACCESS_TOKEN_TO_MAS_MIE     = 'wI2vAZjkFJmghsKS1uem1vFmxnLw3vGcHgkP1SGhNtd'
        # to 晴香・美枝子
        ACCESS_TOKEN_TO_MAS_HAR_MIE = 'ncRbkDHsTP8rx12InMZE25dS3fFk1aoecVWUESB9Pag'

        # トークン設定
        if self.send_name == '美枝子':
            t_access_token = ACCESS_TOKEN_TO_MAS_MIE
        elif self.send_name == '晴香・美枝子':
            t_access_token = ACCESS_TOKEN_TO_MAS_HAR_MIE
        else:
            raise Exception('Destination not found !')

        # LINE 送信
        t_errmsg = line_notify(t_access_token, self.send_msg)
        if t_errmsg == '':
            self.end_ok = True
            self.end_msg = self.send_name + 'に' + '\n\n' + \
                           self.send_msg + '\n\n' + \
                           'を送信しました。'
        else:
            self.end_ok = False
            self.end_msg = self.send_name + 'への送信に失敗しました。'

        # 終了画面
        Clock.schedule_once(self.end_screen, 0.5)

    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    #        終了画面
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    ## def end_result(self, p_msg, p_ok=True):
    def end_screen(self, p_dt):
        # 終了画面に切替
        self.manager.current = 'end'

        if self.end_ok:
        # 通常画面
            # 背景色の指定
            self.manager.current_screen.bef_rgba = BG_BLUE
        else:
        # エラー画面
            # 背景色の指定
            self.manager.current_screen.bef_rgba = BG_RED
        # テキスト設定
        self.manager.current_screen.ids.label_msg.text = self.end_msg

        # バイブ
        cssys.adr_vib(1)
        return

#---------------------------------------------------------------------------------
#                   App
#---------------------------------------------------------------------------------
def MainWidget():    # Root Widget
        t_sm = ScreenManager()
        t_sm.add_widget(TopScreen  (name='top'    ))
        t_sm.add_widget(BusyScreen (name='busy'    ))
        t_sm.add_widget(EndScreen  (name='end'     ))

        # 画面切替
        if MENU_ENABLED:
            t_sm.current = 'top'
        else:
            t_sm.current = 'busy'
        return t_sm

class MainApp(App):
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    #            コンストラクタ
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)
        # super().__init__(**kwargs)
        self.title = APP_NAME

    def build(self):    # Root Widget
        return MainWidget()

#---------------------------------------------------------------------------------
#                   Run
#---------------------------------------------------------------------------------
if __name__ == '__main__':
    MainApp().run()
