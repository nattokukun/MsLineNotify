# -*- coding: utf-8 -*-
#//////////////////////////////////////////////////////////////////////////////
#            csuix Custom uix
#            M.Ida 2022.03.07
#//////////////////////////////////////////////////////////////////////////////
#------------------------------------------------------------------------------
#                    インポート
#------------------------------------------------------------------------------
from kivy.uix.screenmanager import Screen
from kivy.graphics import Rectangle
from kivy.graphics import Color
from kivy.clock import Clock
from functools import partial
import threading

# ユーザーライブラリ
from _userlib import cssys
from _userlib.cssys import debug_log
from _userlib import csstr

#---------------------------------------------------------------------------------
#            ウィジット 全childループ クラス
#---------------------------------------------------------------------------------
"""
               ids と children について
    【ids】
        kvファイルを順に読み込んだ時に、一度で読める　id は、
        階層になっていても見える
        しかし、別定義になっている id は、階層関係なく見えない

    【children】
        階層の子供は全く見えない
"""
class WidgetChildLoop():
    def __init__(self, p_main_form,         # メインformまたはscreen
                       p_parent_widget,     # Boxlayout等の親ウイジット
                       p_on_child,          # 子ウイジット毎の関数
                       p_debug = False,
                       **kwargs):

        super(WidgetChildLoop, self).__init__(**kwargs)

        self.main_form = p_main_form
        self.parent_widget = p_parent_widget
        self.on_child = p_on_child
        self.debug = p_debug

        # メインformからの全idリストをクリア
        self.__all_id_insts = None

        """
        # インスタンス辞書初期化
        self.inst_dict = None
        """
    @property
    def all_id_insts(self):
        if self.__all_id_insts == None:
        # メインformからの全idリストを作成
            if self.debug:
                print('**** all_id_insts start ***')
            self.__all_id_insts = {}
            self.__store_all_id_insts_staff(self.main_form, '')
            if self.debug:
                print('**** all_id_insts end ***')
        return self.__all_id_insts

    def __store_all_id_insts_staff(self, p_widget,
                                         p_name_top):
        ROUTIN = '__store_all_id_insts_staff.. '
        # ids をストアする
        for t_id_name, t_inst in p_widget.ids.items():
            if p_name_top == '':
                t_name = t_id_name
            else:
                t_name = p_name_top + ':' + t_id_name

            if self.debug:
                print(t_name)
            # 追加
            ### self.__all_id_insts[t_name] = t_inst
            self.__all_id_insts[t_inst] = t_name

        # 子供を調査
        for t_widget in reversed(p_widget.children):
            # t_widget に対する id名を探す
            try:
                t_widget_name = self.__all_id_insts[t_widget]
            except:
                t_widget_name = ''
            t_name_top = p_name_top + ':' + t_widget_name
            self.__store_all_id_insts_staff(t_widget, t_name_top)

    """
    # id_nameストア
    def __store_id_name(self, p_widget):
        ""
            以下では、itemsが、親に追加されている場合がある
        ""
        if self.debug:
            t1 = len(p_widget.children)
            t2 = len(p_widget.ids.items())
            if t1 != t2:
                print(f'diff.. {p_widget} c {t1} :i {t2}')
            else:
                print(f'same.. {p_widget} c {t1} :i {t2}')
        if self.debug:
            print(f'*** store top.. {p_widget}')
        # 直下のid_nameをストアする
        for t_id_name, t_inst in p_widget.ids.items():
            if self.debug:
                print(f'store .. {t_id_name} : {t_inst}')
            self.inst_dict[t_inst] = t_id_name
        # 子供を調査する
        for t_inst in p_widget.children:
            self.__store_id_name(t_inst)
    """

    # インスタンス処理
    def __inst_staff(self, p_inst):
        """
        if self.debug:
            print('**** all inst_dict *****')
            print('*********')
        """
        """
        try:
            # インスタンス辞書から id_name を得る
            t_id_name = self.inst_dict[p_inst]
            t_name = t_id_name
        except:
        # id_name 無し
            t_id_name = ''
            t_name = csstr.spc(10)
        """
        # id名を求める
        try:
            t_id_name_ext = self.all_id_insts[p_inst]
        except:
            t_id_name_ext = ''
        if self.debug:
            debug_log(f'__inst_staff.. {t_id_name_ext} {p_inst}')
        if self.on_child != None:
            ## self.on_child(p_inst, t_id_name)
            self.on_child(p_inst, t_id_name_ext)

    # childループ
    def __child_loop(self, p_widget,
                           p_level):
        ## print('****')
        ## print(f'{p_level} : child count.. {len(p_widget.children)}')
        ## t_ctr = 0

        """
        ## if self.debug:
        t1 = len(p_widget.children)
        t2 = len(p_widget.ids.items())
        if t1 < t2:
            print(f'diff222.. {p_widget} {t1}:{t2}')
        """

        # 直下の子インスタンスを children からストア
        t_insts = [t_inst for t_inst in reversed(p_widget.children)]

        """
            子供として来ない事がある
            例
                PopupMenuBox:
                    floatlayout:
                        contextmenu:
            の場合
                PopupMenuBox の子は 1
                    floatlayout の子は 0
            となり
                PopupMenuBox の ids は
                    floatlayout
                    contextmenu
            となる
        """
        # 不足があれば追加する
        # 直下の子インスタンスを items からストア
        for t_id_name, t_inst in p_widget.ids.items():
            try:
                t_idx = t_insts.index(t_inst)
            except:
            # 存在しない
                ### 順番がやばい
                t_insts.append(t_inst)
        # 改めて
        # 全インスタンスループ
        for t_inst in t_insts:
            ## t_ctr += 1
            # インスタンス処理
            self.__inst_staff(t_inst)
            if len(t_inst.children) > 0:
            # 子供がいた
                ## print('    hit child')
                # childループ
                self.__child_loop(t_inst, (p_level + 1))
            else:
                ## print('    child none')
                pass

    # ループ実行
    def execute(self):
        """
        if self.inst_dict == None:
        # インスタンス辞書作成
            self.inst_dict = {}

            t1 = len(self.parent_widget.children)
            t2 = len(self.parent_widget.ids.items())
            if t1 < t2:
                print(f'diff.. {self.parent_widget} {t1}:{t2}')
            ""
            # id_nameストア
            self.__store_id_name(self.parent_widget)
            ""
            if t1 < t2:
                print(f'   dict count.. {len(self.inst_dict)}')
                for t_inst, t_name in self.inst_dict.items():
                    print(f'   {t_inst} = {t_name}')
        """

        ## debug_log(f'__inst_staff.. ******** start ********')
        # childループ
        self.__child_loop(self.parent_widget, 1)
        ## debug_log(f'__inst_staff.. ********  end  ********')
#---------------------------------------------------------------------------------
#            ウィジット 全childのインスタンス・id_name辞書の取得
#---------------------------------------------------------------------------------
class WidgetChildData():
    def __init__(self, p_main_form,                 # メインformまたはscreen
                       p_parent_widget = None,      # Boxlayout等の親ウイジット
                       p_debug = False,
                       **kwargs):

        if p_parent_widget == None:
            p_parent_widget = p_main_form

        super(WidgetChildData, self).__init__(**kwargs)
        self.widget_child_loop = WidgetChildLoop(p_main_form, p_parent_widget,
                                                 self.__on_child, p_debug)
        self.debug = p_debug
        """
        if p_debug:
            t1 = len(p_parent_widget.children)
            t2 = len(p_parent_widget.ids.items())
            print(f'{p_parent_widget} {t1}:{t2}')
        """

        # インスタンス：id名 辞書作成
        self.inst_name_ext_dict = {}
        self.widget_child_loop.execute()

        if self.debug:
            print('************   WidgetChildData  **********')
            for t_inst, t_id_name in self.inst_name_ext_dict.items():
                print(f'{t_inst} name={t_id_name}')
            print('')

        # インスタンスリストクリア
        self.__insts = None

        # id名・インスタンス辞書クリア
        self.__uniq_name_inst_dict = None

        # id名リストクリア
        self.__uniq_id_names = None

    @property
    def insts(self):
        if self.__insts == None:
            self.__insts = list(self.inst_name_ext_dict.keys())
        return self.__insts

    # t_id_name_ext から t_id_name を得る
    def __id_name_ext_to_id_name(self, p_id_name_ext):
        t_texts = p_id_name_ext.split(':')
        t_id_name = t_texts[len(t_texts)-1]
        return t_id_name

    @property
    def uniq_name_inst_dict(self):
        if self.__uniq_name_inst_dict == None:
            """
            if self.debug:
                print(f'**** uniq_name_inst_dict.. count.. {len(self.inst_name_ext_dict.items())}')
            """
            t_delete_uniq_id_names = []
            self.__uniq_name_inst_dict = {}
            for t_inst, t_id_name_ext in self.inst_name_ext_dict.items():
                if t_id_name_ext != '' and \
                   t_id_name_ext !=    None:
                    """
                    # t_id_name_ext から t_id_name を得る
                    t_texts = t_id_name_ext.split(':')
                    t_id_name = t_texts[len(t_texts)-1]
                    """
                    # t_id_name_ext から t_id_name を得る
                    t_id_name = self.__id_name_ext_to_id_name(t_id_name_ext)
                    try:
                        self.__uniq_name_inst_dict[t_id_name] = t_inst
                    except:
                    # 重複している
                        # 削除リストに登録する
                        try:
                            t_delete_uniq_id_names.append(t_id_name)
                        except:
                            pass
            # 削除リストから 重複分を消す
            for t_id_name in t_delete_uniq_id_names:
                self.__uniq_name_inst_dict.pop(t_id_name)

        return self.__uniq_name_inst_dict

    @property
    def uniq_id_names(self):
        if self.__uniq_id_names == None:
            self.__uniq_id_names = list(self.uniq_name_inst_dict.keys())
        return self.__uniq_id_names

    # 子インスタス毎の処理
    def __on_child(self, p_inst,
                         p_id_name_ext):
        """
        if self.debug:
            print('         add = ' + p_id_name_ext)
        """
        self.inst_name_ext_dict[p_inst] = p_id_name_ext

    # アクティブ コントロールを得る
    def get_active_control(self, p_log = False):    # True:ログ出力する
                                                        # アクティブ id名.. id名が''の場合もある
                                                        # アクティブ idインスタンス
        # インスタンス：id名ループ
        for t_inst, t_id_name_ext in self.inst_name_ext_dict.items():
            try:
                if t_inst.focus:
                # フォーカスが有る
                    # t_id_name_ext から t_id_name を得る
                    t_id_name = self.__id_name_ext_to_id_name(t_id_name_ext)
                    return t_id_name, t_inst
            except:
                pass
        # 存在しない
        return '', None

    # id名からidインスタンスを得る
    def id_name_to_inst(self, p_id_name,        # id名
                              p_log = False):   # True：全id名を表示する
                                                    # idインスタンス (id名が重複の場合はNone)
        return self.uniq_name_inst_dict[p_id_name]

    # idインスタンスからid名を得る
    def id_inst_to_name(self, p_inst,           # idインスタンス
                              p_log = False):   # True：全id名を表示する
                                                    # id名 (id名が重複の場合は'')
        t_id_name_ext = self.inst_name_ext_dict[p_inst]
        # t_id_name_ext から t_id_name を得る
        t_id_name = self.__id_name_ext_to_id_name(t_id_name_ext)
        return t_id_name

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
    from _userlib import textinput4ja


"""
###
# アクティブ コントロールを得る
def get_active_control(p_widget,    # 親widget (Boxlayout等は使用できない?)
                       p_log=False):# True:ログ出力する
                                    # アクティブ id名
                                    # アクティブ idインスタンス
    ROUTIN = 'get_active_control.. '

    # 子供があるインスタンスリスト
    t_parent_insts = []
    if p_log:
        debug_log(ROUTIN + '** ids.items **')
        t_count = 0

    t_id_name_act = ''
    t_id_inst_act = None
    # ids ループ
    for t_id_name, t_id_inst in p_widget.ids.items():
        if p_log:
            t_count += 1
            debug_log(ROUTIN + f'{t_count}:{t_id_name}')
        try:
            if t_id_inst.focus:
            # フォーカスが有る
                t_id_name_act = t_id_name
                t_id_inst_act = t_id_inst
                break
            else:
            # フォーカスが無い.. 子供があるインスタンスをストアする
                pass
        except:
        # インスタンス例外.. 子供があるインスタンスをストアする
            pass

        # 子供があるインスタンスをストアする
        if len(t_id_inst.children) > 0:
        # 子供がある
            t_parent_insts.append(t_id_inst)
            if p_log:
                debug_log(ROUTIN + f'{t_id_name} is have childs')

    if t_id_inst_act == None:
    # アクティブが無い
        # 子供を見る
        for t_inst in t_parent_insts:
            t_id_name_act, t_id_inst_act = get_active_control(t_inst, p_log)
            if t_id_inst_act != None:
            # アクティブが見つかった
                break

    return t_id_name_act, t_id_inst_act
"""

"""
###
# id名からidインスタンスを得る
def id_name_to_inst(p_widget,       # 親widget (Boxlayout等は使用できない?)
                    p_id_name,      # id名
                    p_log = False): # True：全id名を表示する
                                    # idインスタンス
    ROUTIN = 'id_name_to_inst.. '

    # 子供があるインスタンスリスト
    t_parent_insts = []

    if p_log:
    # True：全id名を表示する
        t_idx = 0
        debug_log('')
        debug_log(ROUTIN + f'all name list parent is {p_widget}')
        debug_log(ROUTIN + f'children count.. {len(p_widget.children)}')
        for t_inst in p_widget.children:
            debug_log(f'{t_inst}')

    t_id_inst_ret = None
    for t_id_name, t_id_inst in p_widget.ids.items():
        if p_log:
        # True：全id名を表示する
            t_idx += 1
            debug_log(ROUTIN + f'{t_idx} = {t_id_name}')

        if t_id_name == p_id_name:
            t_id_inst_ret = t_id_inst
            break

        # 子供があるインスタンスをストアする
        if len(t_id_inst.children) > 0:
        # 子供がある
            t_parent_insts.append(t_id_inst)
            if p_log:
                debug_log(ROUTIN + f'{t_id_name} is have childs')

    if t_id_inst_ret == None:
    # 該当が無い
        # 子供を見る
        for t_inst in t_parent_insts:
            t_id_inst_ret = id_name_to_inst(t_inst, p_id_name, p_log)
            if t_id_inst_ret != None:
            # 該当が見つかった
                break

    return t_id_inst_ret
"""

"""
###
# idインスタンスからid名を得る
def id_inst_to_name(p_widget,       # 親widget (Boxlayout等は使用できない?)
                    p_id_inst,      # idインスタンス
                    p_log = False): # True：全id名を表示する
                                    # id名
    ROUTIN = 'id_inst_to_name.. '

    # 子供があるインスタンスリスト
    t_parent_insts = []

    if p_log:
    # True：全id名を表示する
        t_idx = 0
        debug_log(ROUTIN + 'all name list')

    t_id_name_ret = ''
    for t_id_name, t_id_inst in p_widget.ids.items():
        if p_log:
        # True：全id名を表示する
            t_idx += 1
            debug_log(ROUTIN + f'{t_idx} = {t_id_name}')
        try:
            if t_id_inst == p_id_inst:
                t_id_name_ret = t_id_name
                break
            else:
                pass
        except:
            pass

        # 子供があるインスタンスをストアする
        if len(t_id_inst.children) > 0:
        # 子供がある
            t_parent_insts.append(t_id_inst)
            if p_log:
                debug_log(ROUTIN + f'{t_id_name} is have childs')

    if t_id_name_ret == '':
    # アクティブが無い
        # 子供を見る
        for t_inst in t_parent_insts:
            t_id_name_ret = id_inst_to_name(t_inst, p_id_inst, p_log)
            if t_id_name_ret != '':
            # アクティブが見つかった
                break

    return t_id_name_ret
"""

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
INPUT_FLD_MARK = '*F*'
INPUT_KEY_MARK = 'K'
INPUT_DAT_MARK = 'D'

# id_names キー項目指定テキスト
def input_key_fld_no(p_fld_no): # 入力順番号
    return INPUT_FLD_MARK + INPUT_KEY_MARK + str(p_fld_no)

# id_names データ項目指定テキスト
def input_data_fld_no(p_fld_no): # 入力順番号
    return INPUT_FLD_MARK + INPUT_DAT_MARK + str(p_fld_no)

# 素の id_names にデータ項目指定テキストを付加する
def input_id_names_add_data_seq(p_id_names):    # 素のid_names
                                                # 付加したid_names
    t_id_names = []
    t_ctr = 0
    for t_id_name in p_id_names:
        t_ctr += 1
        t_id_name = t_id_name + input_data_fld_no(t_ctr)
        t_id_names.append(t_id_name)
    return t_id_names

class InputControl():
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    #            初期化
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    ## def __init__(self, p_widget): # 親widget
    # InputControl()
    def __init__(self, p_widget,                    # 親widget
                       p_input_id_names = None):    # 入力id名リスト

        ROUTIN = 'InputControl __init__ : '

        self.parent = p_widget

        self.input_id_names = p_input_id_names

        self.__parent_child_data = None

        # キー値の入力終了イベントハンドラ
        self.on_key_input_enter = None

        # フィルター切り替えハンドラ
        self.filter_switch = None

        # 個別入力チェックルーチン
        self.individual_input_check = None
        # 総合(個別を除く)入力チェックルーチン
        self.general_input_check = None

        # スコア入力の背景色設定ルーチン
        self.set_input_bgcolor = None
        # 入力フォーカスルーチン
        self.on_input_focus_custom = None

        """
        # メッセージid名
        self.msg_id_name = ''
        # メッセージラベル
        """
        self.label_msg = None

        """
        # フィルターid名
        self.filter_input_id_name    = ''
        self.filter_checkbox_id_name = ''
        """
        # フィルターインスタンス
        self.input_filter    = None
        self.checkbox_filter = None
        self.input_filter_id_name = ''

    # プライベート
        # 再入力idインスタンス
        self.__reinput_id_inst = None

    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    #           プロパティ
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    @property
    # InputControl()
    def parent_child_data(self):
        if self.__parent_child_data == None:
            self.__parent_child_data = WidgetChildData(self.parent)
        return self.__parent_child_data

    @property
    # InputControl()
    def input_id_names(self):
        return self._input_id_names

    @input_id_names.setter
    # InputControl()
    def input_id_names(self, p_value):
        ROUTIN = 'input_id_names.. '
        """
                キー項目     K1 K2
                データ項目    D1 D2 D3

                画面
                            K2
                            D1
                            D3

                input_uniq_id_names        K2 D1 D3
                input_key_id_names    K2
                fld_nos                0  1  3
                key_fld_nos            2

            # 上記を踏まえ データ入力idリスト 設定例
            p_input_uniq_id_names = []
            p_input_uniq_id_names.append('input_code'   + input_key_fld_no(2))
            p_input_uniq_id_names.append('input_name'   + input_data_fld_no(1))
            p_input_uniq_id_names.append('input_age'    + input_data_fld_no(3))
        """

        # とりあえず初期化
        self._input_id_names    = []
        self.input_key_id_names = []
        self.fld_nos            = []    # 0はキーである
        self.key_fld_nos        = []    # 当該 idx の input_key_id_names の項目が、フィールド番号の何番であるか
                                        # input_key_id_names が, key1, key3, key2 の場合
                                        # フィールド番号は、1,3,2 となる
        if p_value == None:
            self._input_id_names = None
            return

        if len(p_value) == 0:
            return

        # 要素の中身を分析し格納する
        for t_id_name in p_value:
            t_names = t_id_name.split(INPUT_FLD_MARK)
            """
            if len(t_names) > 1:
            # キー
                # キーid名
                self.input_key_id_names.append(t_names[0])
                # キーフィールド番号
                t_key_fld_no = int(t_names[1])
                self.key_fld_nos.append(t_key_fld_no)
            """
            t_ok = False
            if len(t_names) == 2:
                t_no_texts = t_names[1].split(INPUT_KEY_MARK)
                if len(t_no_texts) == 2:
                # キー
                    try:
                        # キーid名
                        self.input_key_id_names.append(t_names[0])
                        # キーfld番号
                        t_key_fld_no = int(t_no_texts[1])
                        self.key_fld_nos.append(t_key_fld_no)

                        t_data_fld_no = 0   # キーの場合は0
                        t_ok = True
                    except:
                        pass
                else:
                # キー以外
                    t_no_texts = t_names[1].split(INPUT_DAT_MARK)
                    if len(t_no_texts) == 2:
                    # データ
                        try:
                            t_data_fld_no = int(t_no_texts[1])
                            t_ok = True
                        except:
                            pass

                self.fld_nos.append(t_data_fld_no)

            if not t_ok:
                raise Exception(ROUTIN + f'p_input_id_names is syntax error! ({t_names})')
            # 入力id名
            self._input_id_names.append(t_names[0])

    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    #           絞込インスタンス設定
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    """
    def set_filter_control(self, p_input_id_name,       # フィルターテキストid名
                                 p_checkbox_id_name):   # フィルターチェックボックスid名
        self.filter_input_id_name    = p_input_id_name
        self.filter_checkbox_id_name = p_checkbox_id_name
    """
    """
    def set_filter_control(self, p_input_filter,       # 入力フィルター
                                 p_checkbox_filter):   # チェックボックスフィルター
        self.input_filter    = p_input_filter
        self.checkbox_filter = p_checkbox_filter
    """
    # InputControl()
    def set_filter_control(self, p_input_id_name,       # フィルターテキストid名
                                 p_checkbox_id_name):   # フィルターチェックボックスid名
        ## self.input_filter    = id_name_to_inst(self.parent, p_input_id_name)
        self.input_filter    = self.parent_child_data.id_name_to_inst(p_input_id_name)
        ## self.checkbox_filter = id_name_to_inst(self.parent, p_checkbox_id_name)
        self.checkbox_filter = self.parent_child_data.id_name_to_inst(p_checkbox_id_name)
        self.input_filter_id_name = p_input_id_name

    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    #           当該id名がキーであるか
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # InputControl()
    def is_key(self, p_id_name):    # id名
                                    # True:キーである
        return (p_id_name in self.input_key_id_names)

    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    #        当該id名がキーでキー最後の入力項目か
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # InputControl()
    def is_last_key(self, p_id_name):    # id名
                                    # True:キー最後の入力項目
        t_count = 0
        for t_id_name in self.input_key_id_names:
            t_count += 1
            if p_id_name == t_id_name:
                t_last = (t_count == len(self.input_key_id_names))
                return t_last
        # キーではない
        return False

    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    #       当該id名のキーフィールド番号を得る
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # InputControl()
    def id_name_to_key_fld_no(self, p_id_name): # id名
                                                # キーフィールド番号 <=0:キーとして画面に存在しない
        try:
            t_idx = self.input_key_id_names.index(p_id_name)
            return self.key_fld_nos[t_idx]
        except:
            return -1

    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    #       当該id名のデータフィールド番号を得る
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # InputControl()
    def id_name_to_data_fld_no(self, p_id_name):    # id名
                                                    # データフィールド番号 <=0:データとして画面に存在しない
        try:
            t_idx = self.input_id_names.index(p_id_name)
            return self.fld_nos[t_idx]
        except:
            return -1

    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    #       キーフィールド番号から当該id名を得る
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # InputControl()
    def key_fld_no_to_id_name(self, p_key_fld_no):  # キーフィールド番号
                                                    # id名 '':キーとして画面に無い
        # キーフィールド番号を検索する
        try:
            t_idx = self.key_fld_nos.index(p_key_fld_no)
            return self.input_key_id_names[t_idx]
        except:
            return ''

    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    #           メッセージを表示
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<5<<<<<<<<<<<
    # InputControl()
    def put_msg(self, p_msg = ''):   # 表示メッセ－ジ
        """
        if self.msg_id_name == '':
            return
        self.parent.ids[self.msg_id_name].text = p_msg
        """
        if self.label_msg == None:
            return
        self.label_msg.text = p_msg

    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    #            フィルター状態の設定
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # InputControl()
    def set_filter_state(self, p_on):   # True:On
        """
        # チェックボックス状態変更
        if self.filter_checkbox_id_name != '':
            self.parent.ids[self.filter_checkbox_id_name].active = p_on
        # 状態によりInputTextの背景色を変更
        if self.filter_input_id_name != '':
            if p_on:
                t_color = (0.68, 0.91, 0.95, 1) # 水
            else:
                t_color = (0.768, 0.760, 0.956, 1) # 薄青灰
            self.parent.ids[self.filter_input_id_name].background_color = t_color
        """
        # チェックボックス状態変更
        if self.checkbox_filter != None:
            self.checkbox_filter.active = p_on
        # 状態によりInputTextの背景色を変更
        if self.input_filter != None:
            if p_on:
                t_color = (0.68, 0.91, 0.95, 1) # 水
            else:
                t_color = (0.768, 0.760, 0.956, 1) # 薄青灰
            self.input_filter.background_color = t_color

    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    #            フォーカス移動
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # InputControl()
    def __focus_move_next(self, p_id_name_active):   # 現在のid名
        ROUTIN = '__focus_move_next : '
        if self.input_id_names == None:
            debug_log(ROUTIN + 'input_uniq_id_names none!')
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
        # id名が無い
            ## raise Exception(ROUTIN + 'not found ' + p_id_name_active)
            """
            # フィルターid名
            if self.filter_input_id_name != '':
            # フィルターidが存在する
                if self.filter_input_id_name == p_id_name_active:
                # フィルターidである
                    if self.filter_switch == None:
                    # フィルター切り替えハンドラが無い
                        raise Exception(ROUTIN + 'filter_switch no handler ')
                    self.filter_switch(True, self.parent.ids[p_id_name_active].text)
            """
            """
            if self.input_filter != None:
            # フィルターが有効である
                # アクティブインスタンスを得る
                t_inst_active = id_name_to_inst(self.parent, p_id_name_active)
                if t_inst_active == None:
                    raise Exception(ROUTIN + 'not found input_filter instance')

                if self.input_filter == t_inst_active:
                # フィルターidである
                    if self.filter_switch == None:
                    # フィルター切り替えハンドラが無い
                        raise Exception(ROUTIN + 'filter_switch no handler ')
                    self.filter_switch(True, self.input_filter.text)
            """
            # フィルターid名
            if self.input_filter_id_name != '':
            # フィルターidが存在する
                if self.input_filter_id_name == p_id_name_active:
                # フィルターidである
                    if self.filter_switch == None:
                    # フィルター切り替えハンドラが無い
                        raise Exception(ROUTIN + 'filter_switch no handler ')
                    self.filter_switch(True, self.input_filter.text)
            return

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
    # InputControl()
    def all_input_check(self):
                                # エラーメッセージ '':OK
        # 個別チェック
        if self.individual_input_check != None:
            # 個別入力チェックループ
            for t_id_name in self.input_id_names:
                # id名からidインスタンスを得る
                ## t_id_inst = id_name_to_inst(self.parent, t_id_name)
                t_id_inst = self.parent_child_data.id_name_to_inst(t_id_name)
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
    # Android用処理
    #    ・read only input フィールドを選択状態にすると他のフィールドに移動しても
    #     選択状態が消えないので、それを消すための処理
    # InputControl()
    def __on_input_enter_android(self):
        # read only のフィールドを探す
        for t_id_name, t_id_inst in self.parent.ids.items():
            t_ro = False
            try:
                if t_id_inst.readonly:
                    t_ro = True
            except:
                pass
            if t_ro:
            # read only である
                t_id_inst.cancel_selection()
                ## print('read only = ' + t_id_name)
            else:
                ## print('no = ' + t_id_name)
                pass

    # InputControl()
    def on_input_enter(self):
        # Android用処理
        self.__on_input_enter_android()

        # アクティブを得る
        ## t_id_name, t_id_inst = get_active_control(self.parent, False)
        t_id_name, t_id_inst = self.parent_child_data.get_active_control()
        if t_id_inst == None:
        # インスタンスが無い
            return

        t_ok = True
    #　キー値であれば キー値何れかに相違があれば データ移動が必要
        if self.is_key(t_id_name):
        # キー項目である
            # キー値の入力終了イベントハンドラ
            if self.on_key_input_enter != None:
                t_errmsg = self.on_key_input_enter(t_id_name, t_id_inst,
                                                   t_id_inst.text)
                self.put_msg(t_errmsg)
                t_ok = (t_errmsg == '')
        if t_ok:
            # 個別入力チェックルーチン
            if self.individual_input_check != None:
                t_errmsg = self.individual_input_check(t_id_name, t_id_inst,
                                                       t_id_inst.text)
                self.put_msg(t_errmsg)
                t_ok = (t_errmsg == '')
            ## else:
            ##     t_ok = True

        if not t_ok:
        # エラー
            # 再入力インスタンスを保存する
            self.__reinput_id_inst = t_id_inst
            return

        # 正常値
        ## self.put_msg()

        # 次にフォーカス移動
        self.__focus_move_next(t_id_name)

    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    #        入力フォーカスイベント debug
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # InputControl()
    def on_input_focus_debug(self, p_id_inst,   # idインスタンス
                                   p_msg):      # メッセージ
        ## FOCUS_DEBUG = True
        FOCUS_DEBUG = False

        if FOCUS_DEBUG:
            # idインスタンスからid名を得る
            ## t_id_name = id_inst_to_name(self.parent, p_id_inst)
            t_id_name = self.parent_child_data.id_inst_to_name(p_id_inst)
            print("'" + t_id_name + "'" + '  ' + p_msg)

    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    #        入力フォーカスイベント
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # InputControl()
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
    # InputControl()
    def set_focus_top(self):
        if self.input_id_names == None:
            debug_log('set_focus_top : ' + 'input_uniq_id_names is None!')
            return

        t_id_name = self.input_id_names[0]

        self.parent.ids[t_id_name].focus = True
        ## print('focus on executed : ' + t_id_name)

        # xx/xx/xx
        # 上記1行では focus off になることがあるので、インターバルをおいて
        # off であれば再度 on にする
        focus_at_intervals(self.parent.ids[t_id_name], 0) # no boo
##
