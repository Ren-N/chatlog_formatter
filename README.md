# chatlog_formatter
====

チャットツールのバックアップ用テキストファイルを見やすいようにHTML/CSSに変換する．現在はLINEのみに対応．

## Requirement

次の環境で動作を確認済み．
 - Python 2.7.10
 - OS X El Capitan Version10.11.5

## Usage
clog2html.pyと同じディレクトリにtemplateディレクトリを置いておく．
clog2html.pyにテキストファイルを引数に渡して実行する．[-name]でチャットツールの自分のアカウント名を指定する．
ディレクトリ内にindex.htmlを含むディレクトリが生成される．

'''
$ python clog2html.py FILE.txt [-name] (<AccountName>)
'''

### Example
'''
$ python clog2html.py \[LINE\]\ Testのトーク.txt -name 'Ren-N'
'''

## License

[MIT](https://github.com/tcnksm/tool/blob/master/LICENCE)

## Author

[Ren-N](https://github.com/Ren-N)

## ScreenShot

![ScreenShot](https://github.com/Ren-N/chatlog_formatter/images/sample.png)
