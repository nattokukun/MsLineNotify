# -*- coding: utf-8 -*-
#//////////////////////////////////////////////////////////////////////////////
#            linebot  LINE bot
#            M.Ida 2023.02.15
#//////////////////////////////////////////////////////////////////////////////
#    【注意】
#    Windowsの場合は、以下はコンダプロンプトから実行
#
#    Eclipse から実行する場合は、以下の追加が必要
#    :環境変数 path
#    %USERPROFILE%\Anaconda3
#    %USERPROFILE%\Anaconda3\scripts
#    %USERPROFILE%\Anaconda3\Library\bin
#
"""
    【LINE トークン作成方法】

    PythonでLINEにメッセージを送る
    https://qiita.com/moriita/items/5b199ac6b14ceaa4f7c9

    1) LINE Notify公式にアクセス
    https://notify-bot.line.me/ja/

    2) 右上からログイン

    3) ログインと同じところをクリックし，マイページへ

    4) ページ下部の「トークンを発行」をクリック

    5) ページ上部でちゃんと連携されているか確認

    6) スマホのラインで、当該グループにline Notiyfy を招待してやる
"""

import requests

#------------------------------------------------------------------------------
#                   定数定義
#------------------------------------------------------------------------------
API_LINE_NOTIFY_URL = 'https://notify-api.line.me/api/notify'

#------------------------------------------------------------------------------
#                   送信botクラス
#------------------------------------------------------------------------------
class LINENotifyBot:
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    #            コンストラクタ
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    def __init__(self, p_access_token): # アクセストークン
        self.__headers = {'Authorization': 'Bearer ' + p_access_token}

    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    #            送信
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    def send(self, p_message,                   # メッセージ
                   p_image=None,                # 画像ファイル名
                   p_sticker_package_id=None,   # スタンプパッケージID
                   p_sticker_id=None):          # スタンプID
                                                # エラーメッセージ '':成功
        t_payload = {
            'message'           :p_message,
            'stickerPackageId'  :p_sticker_package_id,
            'stickerId'         :p_sticker_id,  }

        t_files = {}
        if p_image != None:
            t_files = {'imageFile': open(p_image, 'rb')}

        try:
            t_ret = requests.post(API_LINE_NOTIFY_URL,
                                  headers = self.__headers,
                                  data = t_payload,
                                  files = t_files,  )
            t_errmsg = ''
        except:
            t_errmsg = 'LINENotifyBot send failed!'

        return t_errmsg
