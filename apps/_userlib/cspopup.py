# -*- coding: utf-8 -*-
#//////////////////////////////////////////////////////////////////////////////
#            cspopup    Custom Pop up
#            M.Ida 2022.08.02
#//////////////////////////////////////////////////////////////////////////////
from kivy.uix.popup import Popup
from kivy.properties import StringProperty
from kivy.lang.builder import Builder

#------------------------------------------------------------------------------
#                   Kv ファイル
#------------------------------------------------------------------------------
Builder.load_string('''
#<KvLang>

# /////////////////////////////////////////////////////////////////////////////
# yes no popup
<YesNoPopup>:

    ## title: 'Confirmation'
    title: app.title

    size_hint: 0.8, 0.3
    pos_hint: {'x':0.1, 'y':0.35}

    FloatLayout:
        Label:
            size_hint: 0.8, 0.6
            pos_hint: {'x': 0.1, 'y':0.4}
            text: root.message

        Button:
            size_hint: 0.4, 0.35
            ## pos_hint: {'x':0.1, 'y':0.05}
            pos_hint: {'x':0.08, 'y':0.05}
            text: 'Yes'
            on_release: root.dispatch('on_yes')

        Button:
            size_hint: 0.4, 0.35
            ## pos_hint: {'x':0.5, 'y':0.05}
            pos_hint: {'x':0.52, 'y':0.05}
            text: 'No'
            on_release: root.dispatch('on_no')

# /////////////////////////////////////////////////////////////////////////////
<OkPopup>:

    ## title: 'Confirmation'
    title: app.title

    size_hint: 0.8, 0.3
    pos_hint: {'x':0.1, 'y':0.35}

    FloatLayout:
        Label:
            size_hint: 0.8, 0.6
            pos_hint: {'x': 0.1, 'y':0.4}
            text: root.message

        Button:
            ## size_hint: 0.4, 0.35
            size_hint: 0.4, 0.28
            ## pos_hint: {'x':0.1, 'y':0.05}
            ## pos_hint: {'x':0.08, 'y':0.05}
            pos_hint: {'x':0.3, 'y':0.05}
            text: 'Ok'
            on_release: root.dispatch('on_ok')

# /////////////////////////////////////////////////////////////////////////////

#</KvLang>
''')

#------------------------------------------------------------------------------
#                   単独関数
#------------------------------------------------------------------------------
# yes_no_popup_open 使用例
"""
                :
        # ハンドラ内で処理番号にて判定する
        self.proc_no = 10
        # オープン
        cspopup.yes_no_popup_open('execute ok ?', self._popup_yes, self._popup_no)
                :

    イベントハンドラーは自クラスで宣言

    # yes no popup -> yes
    def _popup_yes(self, p_instance):
        print('yes ! no:' + str(self.proc_no))
        p_instance.dismiss()

    # yes no popup -> no
    def _popup_no(self, p_instance):
        p_instance.dismiss()
"""
# yes no popup open
def yes_no_popup_open(p_msg,                  # メッセージ
                      p_popup_yes_handler,
                      p_popup_no_handler):
    # yes no popup
    t_popup = YesNoPopup(
        ## title='Confirmation',
        message = p_msg
        ## size_hint = (0.8, 0.3),
        ## pos_hint  = {'x':0.1, 'y':0.35}
    )
    t_popup.bind(on_yes = p_popup_yes_handler,
                 on_no  = p_popup_no_handler     )
    t_popup.open()

# ok popup open
def ok_popup_open(p_msg,                  # メッセージ
                  p_popup_ok_handler):
    # yes no popup
    t_popup = OkPopup(
        ## title='Confirmation',
        message = p_msg
        ## size_hint = (0.8, 0.3),
        ## pos_hint  = {'x':0.1, 'y':0.35}
    )
    t_popup.bind(on_ok = p_popup_ok_handler)
    t_popup.open()

#------------------------------------------------------------------------------
#                   クラス
#------------------------------------------------------------------------------
# yes no popup
class YesNoPopup(Popup):

    __events__ = ('on_yes', 'on_no')

    message = StringProperty('')

    def __init__(self, **kwargs) -> None:
        super(YesNoPopup, self).__init__(**kwargs)
        self.auto_dismiss = False

    def on_yes(self):
        pass

    def on_no(self):
        pass

# ok popup
class OkPopup(Popup):

    ## __events__ = ('on_ok') # これは実行時エラーとなるので、以下とした
    __events__ = ('on_ok', 'on_ok') # イベントは2つ必要？

    message = StringProperty('')

    def __init__(self, **kwargs) -> None:
        super(OkPopup, self).__init__(**kwargs)
        self.auto_dismiss = False

    def on_ok(self):
        pass
