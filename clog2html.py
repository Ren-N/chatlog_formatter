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
        save_date = lines.pop(0)
        lines.pop(0)

        '''本文'''
        # 日付パターン  e.g. 2016/07/15(金)
        date_pttr    = re.compile(r'20[0-9]{2}/[0-9]{2}/[0-9]{2}\([月火水木金土日]\)'.decode('utf-8'))
        # メッセージ
        chatlog = [] #次の3種類 > DATE:日付 | SYS:システムコメント | MESSEAGE:人のメッセージ
        acc = []
        for line in lines:
            l = line.decode('utf-8')
            #日付
            re_date  = date_pttr.search(l)
            if re_date :
                if len(acc) > 0 :
                    chatlog.extend( _TextToObjectList('MESSAGE',acc) )

                kind = 'DATE'
                data = re_date.group(0)
                chatlog.extend( _TextToObjectList(kind,data) )
                continue
            else:
                acc.append(l)
        # accに残っていればchatlogに追加
        if len(acc) > 0 :
            chatlog.extend( _TextToObjectList('MESSAGE',acc) )
    return (title,chatlog)


def _TextToObjectList(kind, data):
    '''convertChatLog()補助関数.

    kind   : [ 'DATE' | 'MESSAGE' ]
    data   : DATEの時は文字列．MESSAGEの時はリスト．
    return : 行の情報を表すObjectのリストを返す．
    行のObjectの説明 :
        <引数:DATEの時>     (返値の例) [  {'DATE' : '2016/07/15(金)'}  ]
            ラベルとして，'DATE'
            情報として，'2016/07/15(金)'(日付)
            を持つ辞書．
        <引数:MESSAGEの時>  (返値の例) [  {'MESSAGE' : Object}, {'SYS' : Object}, ...  ]
            ラベルとして，'MESSAGE'(人のメッセージ) か 'SYS'(システムコメント)，
            情報として，{'time':発信時間，'who':誰が，'txt':メッセージテキスト}
            を持つ辞書．
    '''
    print(kind)
    # 行パターン  e.g. 18:30[Tab]Ren N[Tab]こんにちわ．
    line_pttr    = re.compile(r'([0-9]{2}:[0-9]{2})\t(.*)'.decode('utf-8'))
    # メッセージパターン  e.g. Ren N[Tab]こんにちわ．
    message_pttr = re.compile(r'(.*?)\t(.*?)'.decode('utf-8')) #これにマッチしない場合(ユーザー名[Tab]がない場合)はシステムコメント．
    # 戻り値
    objectList = []
    '''日付'''
    if kind == 'DATE':
        objectList.append( {'DATE':data} )
        return objectList
    '''メッセージ'''
    # else:
    prev_txt = None
    # print('---------------')
    # print(data)
    # print('---------------')
    for line in data:

        re_line  = line_pttr.search(line)
        if re_line :
            # 前のメッセージがあれば蓄積 ----------
            if prev_txt:
                objectList.append( prev_txt )
                prev_txt = None
            # ---------------------------------
            _time  = re_line.group(1)
            _messe = re_line.group(2)

            re_messe = message_pttr.search(_messe)
            # 人のメッセージ
            if re_messe:
                # print('Messe')
                # print(line)
                _who = re_messe.group(1)
                _txt = re_messe.group(2)
                _kind = 'MESSAGE'
                _data = {'time':_time, 'who':_who, 'txt':_txt}
            # システムコメント
            else:
                # print('Sys')
                # print(line)
                _kind = 'SYS'
                _data = {'time':_time, 'txt':_messe}
            prev_txt = { _kind : _data }
        # メッセージ(複数行の場合．人のメッセージのみ)
        else:
            if prev_txt :
                prev_txt['MESSAGE']['txt'] += '\n'+line
    # メッセージが残っていれば蓄積
    if prev_txt:
        objectList.append( prev_txt )
    return objectList




if __name__ == '__main__':
    # オプション取得
    options = analyzeOptionArgs(sys.argv)
    app = options['-app'] if options.has_key('-app') else 'LINE'
    # chatlogファイルを解析
    chatlog = convertChatLog(options['filename'], app)
    print(chatlog[0])
    print(chatlog[1][0])
