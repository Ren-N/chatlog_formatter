# -*- coding: utf-8 -*-
import sys
import re
# $clog2html.py log.txt -name [user-name] -app [application-name]


def analyzeOptionArgs(argv):
    u'''コマンド引数をOptionの辞書にして返す．

    e.g.
    $ python clog2html.py log.txt -name 'Ren N' -app LINE
    >>> {'filename':log.txt, '-name':'Ren N', '-app':'LINE'}
    '''
    _OPTIONS = ['-name','-app']
    options = {}
    if len(argv) == 1:
        #対話式予定
        print('no arguments.')
        sys.exit()
    else:
        #ファイル名を取得
        if re.match(r'.*?\.txt', argv[1]):
            options['filename'] = argv[1]
        else:
            print('invalid filename.')
            sys.exit()
        #オプションの取得
        for i,arg in enumerate(argv):
            if arg in _OPTIONS:
                # (i+1)が存在し，optionでなければ保存
                if i+1 < len(argv) and not argv[i+1] in _OPTIONS:
                    options[arg] = argv[i+1]
    return options

def convertChatLog(filename, app):
    f = open(filename)
    lines = f.readlines()
    f.close()

    '''LINE'''
    if app in ['LINE','line','Line','ライン']:
        '''タイトル'''
        title = re.search(r'\[LINE\] (.*?)のトーク履歴',lines.pop(0))
        title = title.group(1) if title else ''

        '''保存日時'''
        lines.pop(0)

        '''本文'''
        # 日付パターン  e.g. 2016/07/15(金)
        date_pttr    = re.compile(r'20[0-9]{2}/[0-9]{2}/[0-9]{2}\([月火水木金土日]\)'.decode('utf-8'))
        # 行パターン  e.g. 18:30[Tab]Ren N[Tab]こんにちわ．
        line_pttr    = re.compile(r'([0-9]{2}:[0-9]{2})\t(.*?)'.decode('utf-8'))
        # メッセージパターン  e.g. Ren N[Tab]こんにちわ．
        message_pttr = re.compile(r'(.*?)\t(.*?)'.decode('utf-8')) #これにマッチしない場合(ユーザー名[Tab]がない場合)はシステムコメント．
        # メッセージ  次の3種類 > DATE:日付 | SYS:システムコメント | MESSEAGE:人のメッセージ
        chatlog = []
        tmp = None #複数行にまたぐ場合の一時保存
        for line in lines:
            #日付
            re_date  = date_pttr.search(line)
            if re_date :
                kind = 'DATE'
                data = re_date.group(9)
                chatlog.append( { kind : data } )
                continue
            #メッセージ
            re_line  = line_pttr.search(line)
            if re_line :
                _time  = re_line.group(1)
                _messe = re_line.group(2)
                re_messe = message_pttr.search(_messe)
                if re_messe: # 人のメッセージ
                    _who = re_messe.group(1)
                    _txt = re_messe.group(2)
                    kind = 'MESSAGE'
                    data = {'time':_time, 'who':_who, 'txt':_txt}
                    tmp = { kind : data }
                else:        # システムコメント
                    kind = 'SYS'
                    data = {'time':_time, 'txt':_messe}
                    chatlog.append( { kind : data } )
                    continue
            # メッセージ(2行目以降)
            else:



if __name__ == '__main__':
    # オプション取得
    options = analyzeOptionArgs(sys.argv)
    # chatlogファイルを解析
    chatlog = convertChatLog(options['filename'], options['-app'])
