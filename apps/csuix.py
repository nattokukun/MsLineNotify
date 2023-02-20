# -*- coding: utf-8 -*-
#//////////////////////////////////////////////////////////////////////////////
#            csuix Custom uix
#            M.Ida 2022.03.07
#//////////////////////////////////////////////////////////////////////////////
#------------------------------------------------------------------------------
#                    インポート
#------------------------------------------------------------------------------
from kivy.uix.screenmanager import Screen
from kivy.graphics import Color
from kivy.graphics import Rectangle
from kivy.clock import Clock
from functools import partial
import threading

# ユーザーライブラリ
import cssys
from cssys import debug_log

#------------------------------------------------------------------------------
#                    関数群
#------------------------------------------------------------------------------
# 日本語画面調整
def japanize_screen():
    if cssys.is_windows():
        import japanize_kivy
    else:
        from kivy.core.text import LabelBase, DEFAULT_FONT  # [パターン２] デフォルトの表示フォントを
        from kivy.resources import resource_add_path        #              Userが指定する
        ## LabelBase.register(DEFAULT_FONT, "ipaexg00401/ipaexg.ttf") apkでNG
        resource_add_path("/system/fonts")
        ## LabelBase.register(DEFAULT_FONT, "NotoSansBuhid-Regular.ttf") NG
        LabelBase.register(DEFAULT_FONT, "NotoSansCJK-Regular.ttc")
    import textinput4ja

# アクティブ コントロールを得る
def get_active_control(p_widget):   # 親widget
                                    # アクティブ id名
                                    # アクティブ idインスタンス
    t_id_name_act = ''
    t_id_inst_act = None
    for t_id_name, t_id_inst in p_widget.ids.items():
        try:
            if t_id_inst.focus:
                t_id_name_act = t_id_name
                t_id_inst_act = t_id_inst
                break
            else:
                pass
        except:
            pass
    return t_id_name_act, t_id_inst_act

# id名からidインスタンスを得る
def id_name_to_inst(p_widget,   # 親widget
                    p_id_name): # id名
                                # idインスタンス
    t_id_inst_ret = ''
    for t_id_name, t_id_inst in p_widget.ids.items():
        if t_id_name == p_id_name:
            t_id_inst_ret = t_id_inst
            break
    return t_id_inst_ret

# idインスタンスからid名を得る
def id_inst_to_name(p_widget,   # 親widget
                    p_id_inst): # idインスタンス
                                # id名
    t_id_name_ret = ''
    for t_id_name, t_id_inst in p_widget.ids.items():
        try:
            if t_id_inst == p_id_inst:
                t_id_name_ret = t_id_name
                break
            else:
                pass
        except:
            pass
    return t_id_name_ret

# スレッドで指定ウイジットにフォーカスを与える
# (スレッドを使用するので再描画と重ならない次項目移動に使用する)
def focus_at_intervals(p_id_inst,        # idインスタンス
                       p_boo_sec = 0.2): # cssys.boo 秒 0:鳴らさない

    t_thread = threading.Thread(target=focus_at_intervals_target,
                                args=(p_id_inst, p_boo_sec, ))
    t_thread.start()

def focus_at_intervals_target(p_id_inst,        # idインスタンス
                              p_boo_sec = 0.2): # cssys.boo 秒 0:鳴らさない
    if p_boo_sec <= 0:
    # 鳴らさない
        import time
        ## time.sleep(int(1000 * 0.2)) bug!
        time.sleep(0.2)
    else:
        cssys.boo(p_boo_sec)

    if not p_id_inst.focus:
        p_id_inst.focus = True
    ## print(p_id_inst)

# スレッドで指定カーソルを右端に移動する
def move_right_cursor_intervals(p_id_inst):    # idインスタンス
    """
    t_thread = threading.Thread(target=move_right_cursor,
                                args=(p_id_inst, ))
    t_thread.start()
    """
    # このインターバルも微妙な調整をした結果
    Clock.schedule_once(partial(move_right_cursor, p_id_inst), 0.0011)

def move_right_cursor(p_id_inst, *largs): # idインスタンス
    """
    # このインターバルも微妙な調整した結果
    time.sleep(int(1000 * 0.0015))
    # カーソル位置を最右端に変更 (カーソルを取得する場合もこの程度の間隔が必要)
    p_id_inst.cursor = (100, 0)
    """
    # カーソル位置を最右端に変更 (カーソルを取得する場合もこの程度の間隔が必要)
    p_id_inst.cursor = (100, 0)

#------------------------------------------------------------------------------
#                    カスタムScreen クラス
#------------------------------------------------------------------------------
# 背景の色を変える
#   参照：https://pyky.github.io/kivy-doc-ja/guide/widgets.html#adding-widget-background

class ScreenCustom(Screen):
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    #            コンストラクタ
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    def __init__(self, **kwargs):
        super(ScreenCustom, self).__init__(**kwargs)

        # 色の初期値
        # self.in_rgba = Color(0, 0, 0, 0, mode='bef_rgba')
        self.__bef_rgba = [0, 0, 0, 0, 1]

        # canvasオブジェクトに Color Rectangle 命令を追加
        #    https://pyky.github.io/kivy-doc-ja/guide/graphics.html
        with self.canvas.before:
            # Color命令を追加
            #         in_color_ref にInstructionへの参照をキープ
            self.in_color_ref = Color(0, 0, 0, 0, mode='bef_rgba')
            # Rectanble命令を追加
            #         in_rect_ref にInstructionへの参照をキープ
            self.in_rect_ref = Rectangle(pos =self.pos,
                                         size=self.size)

        # pos size が変更になったら on_update_rect を実行する様に設定
        self.bind(pos =self.on_update_rect)
        self.bind(size=self.on_update_rect)

    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    #            プロパティ
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    @property
    def bef_rgba(self):
        return self.__bef_rgba

    @bef_rgba.setter
    def bef_rgba(self, p_rgba):
        self.__bef_rgba = p_rgba
        """
        print(p_rgba[0])
        print(p_rgba[1])
        print(p_rgba[2])
        print(p_rgba[3])
        print("--------------")
        """
    pass

    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    #            サイズ変更ハンドラ
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    def on_update_rect(self, *args):
        # Color Instructionへの参照の属性に再設定
        self.in_color_ref.r = self.bef_rgba[0]
        self.in_color_ref.g = self.bef_rgba[1]
        self.in_color_ref.b = self.bef_rgba[2]
        self.in_color_ref.a = self.bef_rgba[3]
        # Rectangle Instructionへの参照の属性に再設定
        self.in_rect_ref.pos  = self.pos
        self.in_rect_ref.size = self.size

#------------------------------------------------------------------------------
#                    入力制御クラス
#------------------------------------------------------------------------------
class InputControl:
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    #            初期化
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    def __init__(self, p_widget):   # 親widget
        self.parent = p_widget
        # 全入力id名リスト
        self.input_id_names = None
        # 個別入力チェックルーチン
        self.individual_input_check = None
        # 総合(個別を除く)入力チェックルーチン
        self.general_input_check = None

        # スコア入力の背景色設定ルーチン
        self.set_input_bgcolor = None
        # 入力フォーカスルーチン
        self.on_input_focus_custom = None

        # メッセージラベル
        self.label_msg_id_name = ''
    # プライベート
        # 再入力idインスタンス
        self.__reinput_id_inst = None

    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    #           メッセージを表示
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    def put_msg(self, p_msg = ''):   # 表示メッセ－ジ
        if self.label_msg_id_name == '':
            return
        self.parent.ids[self.label_msg_id_name].text = p_msg

    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    #            フォーカス移動
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    def __focus_move_next(self, p_id_name_active):   # 現在のidインスタンス
        ROUTIN = '__focus_move_next : '

        if self.input_id_names == None:
            debug_log(ROUTIN + 'input_id_names none!')
            return

        # 現在のidを見つけその番号を得る
        t_ok  = False
        t_idx = -1
        for t_id_name in self.input_id_names:
            t_idx += 1
            if t_id_name == p_id_name_active:
                t_ok = True
                break

        if not t_ok:
            raise Exception(ROUTIN + 'not found ' + p_id_name_active)

        ## debug_log(ROUTIN + 'now ' + p_id_name_active)

        # 次を入力とする
        t_input_count = len(self.input_id_names)
        t_idx += 1;
        if t_idx > (t_input_count - 1):
            t_idx = 0;

        t_id_name_next = self.input_id_names[t_idx]

        ## debug_log(ROUTIN + '  next ' + t_id_name_next + ' idx=' + str(t_idx))

        # 次移動
        self.parent.ids[t_id_name_next].focus = True

    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    #            全入力チェックルーチン
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    def all_input_check(self):
                                # エラーメッセージ '':OK
        # 個別チェック
        if self.individual_input_check != None:
            # 個別入力チェックループ
            for t_id_name in self.input_id_names:
                # id名からidインスタンスを得る
                t_id_inst = id_name_to_inst(self.parent, t_id_name)
                # 個別入力チェック
                t_errmsg = self.individual_input_check(t_id_name, t_id_inst,
                                                       t_id_inst.text)
                if t_errmsg != '':
                    self.put_msg(t_errmsg)
                    return t_errmsg

        # 総合入力(個別を除く)チェック
        if self.general_input_check != None:
            t_errmsg = self.general_input_check()
            if t_errmsg != '':
                self.put_msg(t_errmsg)
                return t_errmsg

        ## self.put_msg()
        ## print('all_input_check execute')
        return ''

    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    #            入力終了イベント
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    def on_input_enter(self):
        # アクティブを得る
        ## t_id_name, t_id_inst = csuix.get_active_control(self.parent)
        t_id_name, t_id_inst = get_active_control(self.parent)
        if t_id_inst == None:
            return

        """
        # スコアチェック
        t_text = t_id_inst.text
        t_text.lstrip()
        if t_text == '':
            t_ok = True
        else:
            t_ok = self.score_text_ok(t_text)
        """
        # 個別入力チェックルーチン
        if self.individual_input_check != None:
            t_errmsg = self.individual_input_check(t_id_name, t_id_inst,
                                                   t_id_inst.text)
            self.put_msg(t_errmsg)
            t_ok = (t_errmsg == '')
        else:
            t_ok = True

        if not t_ok:
        # エラー
            # 再入力インスタンスを保存する
            self.__reinput_id_inst = t_id_inst
            """
            # 再入力
            csuix.focus_at_intervals(t_id_inst)
            """
            return

        # 正常値
        ## self.put_msg()

        """
        # 合計計算
        self.total_calc()

        # 全スコアをファイルに書く
        self.all_input_save()
        """

        # 次にフォーカス移動
        self.__focus_move_next(t_id_name)

    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    #        入力フォーカスイベント debug
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    def on_input_focus_debug(self, p_id_inst,   # idインスタンス
                                   p_msg):      # メッセージ
        ## FOCUS_DEBUG = True
        FOCUS_DEBUG = False

        if FOCUS_DEBUG:
            # idインスタンスからid名を得る
            t_id_name = id_inst_to_name(self.parent, p_id_inst)
            print("'" + t_id_name + "'" + '  ' + p_msg)

    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    #        入力フォーカスイベント
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    def on_input_focus(self, p_id_inst, # idインスタンス
                             p_focus):  # True:フォーカスon
        ROUTIN = 'on_input_focus : '

        if p_focus:
            self.on_input_focus_debug(p_id_inst, ROUTIN + 'on-begin')
        else:
            self.on_input_focus_debug(p_id_inst, ROUTIN + 'off-begin')

        if not p_focus:
        # フォーカス消失
            ## debug_log(ROUTIN + '** not focus begin')

            # 再入力の時はスレッド描画されるめ、再描画のタイミングでは
            # エラーとなる事があるため 再入力の時は色変更しない
            if self.__reinput_id_inst == p_id_inst:
            # 再入力である
                ## debug_log(ROUTIN + 'backgroud color change skiped')

                cssys.boo()
                # フォーカスを強制 (再入力)
                p_id_inst.focus = True

                # クリア
                self.__reinput_id_inst = None
            else:
            # 再入力でない
                if self.set_input_bgcolor != None:
                    # スコア入力の背景色設定
                    self.set_input_bgcolor(p_id_inst)
                    ## debug_log(ROUTIN + 'backgroud color changed')
            pass

            if self.on_input_focus_custom != None:
                self.on_input_focus_custom(p_id_inst, False) # off
                """
                # 合計計算
                self.total_calc()

                # 全スコアをファイルに書く
                self.all_input_save()
                """
            ## debug_log(ROUTIN + '** not focus end')
            if p_focus:
                self.on_input_focus_debug(p_id_inst, ROUTIN + 'error step(A)!')
            else:
                self.on_input_focus_debug(p_id_inst, ROUTIN + 'off-end')
            return
        pass

        # フォーカス取得
        ## debug_log(ROUTIN + '** focus begin')

        if self.on_input_focus_custom != None:
            self.on_input_focus_custom(p_id_inst, True) # on
            """
            # idインスタンスからid名を得る
            t_id_name = csuix.id_inst_to_name(self, p_id_inst)

            # 入力id名からセットNoを得る
            t_setno = self.id_name_to_setno(t_id_name)
            if t_setno == 1:
                t_bar_bottom = True  # バーを下げる
            else:
                t_bar_bottom = False # バーを上げる

            # センタースクロールを上下移動
            self.move_scroll_view(t_bar_bottom)
            """
        pass

        # スレッドで指定カーソルを右端に移動する
        #   クリックでフォーカスが来た時に数字の場合はこの方が操作しやすい
        move_right_cursor_intervals(p_id_inst)    # idインスタンス

        ## debug_log(ROUTIN + '** focus end')
        if p_focus:
            self.on_input_focus_debug(p_id_inst, ROUTIN + 'on-end')
        else:
            self.on_input_focus_debug(p_id_inst, ROUTIN + 'error step(B)!')

    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    #        先頭項目をフォーカスとする
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    def set_focus_top(self):
        if self.input_id_names == None:
            debug_log('set_focus_top : ' + 'input_id_names is None!')
            return

        t_id_name = self.input_id_names[0]

        self.parent.ids[t_id_name].focus = True
        ## print('focus on executed : ' + t_id_name)

        # xx/xx/xx
        # 上記1行では focus off になることがあるので、インターバルをおいて
        # off であれば再度 on にする
        focus_at_intervals(self.parent.ids[t_id_name], 0) # no boo
