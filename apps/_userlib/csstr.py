# -*- coding: utf-8 -*-
#//////////////////////////////////////////////////////////////////////////////
#            csstr  String
#            M.Ida 2022.03.04
#//////////////////////////////////////////////////////////////////////////////
#------------------------------------------------------------------------------
#                   関数群
#------------------------------------------------------------------------------
# 文字列を整数に変換(変換エラーの場合は例外)
def str_to_int(p_text,                      # テキスト
               p_raise_exception = True):   # True:例外を発生させる
                                            # 整数
    ROUTIN = 'str_to_int : '
    t_text = p_text.strip()
    if t_text == '':
        t_int = 0
    else:
        try:
            t_int = int(t_text)
        except:
            if p_raise_exception:
            # True:例外を発生させる
                raise Exception(ROUTIN + 'cannot convert to integer ' + \
                                         '"' + t_text + '"')
            else:
                t_int = 0
    return t_int

# 数値をカンマ区切りにする
def num_to_comma(p_num):   # 数値
    ## return '{:,}'.format(p_num)
    return '{:,d}'.format(p_num)

# 空白を指定数だけ生成する
def spc(p_count):   # 文字数
                    # 生成文字列
    return ' ' * p_count

pass