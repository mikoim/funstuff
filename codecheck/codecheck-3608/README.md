# subot v2

[![CircleCI](https://circleci.com/gh/mikoim/codecheck-3608/tree/master.svg?style=shield)](https://circleci.com/gh/mikoim/codecheck-3608/tree/master)

## デプロイ情報
#### サービスURL

- https://subot-v2.arukascloud.io/
- http://subot-v2.miko.im/

#### リポジトリURL

https://github.com/mikoim/codecheck-3608

#### 使用言語

- Python > 3.5

#### 主なライブラリ

| Library    | PyPI URL                                |
|------------|-----------------------------------------|
| PyOWM      | https://pypi.python.org/pypi/pyowm      |
| pytest     | https://pypi.python.org/pypi/pytest     |
| pytz       | https://pypi.python.org/pypi/pytz       |
| redis      | https://pypi.python.org/pypi/redis      |
| rfGengou   | https://pypi.python.org/pypi/rfGengou   |
| websockets | https://pypi.python.org/pypi/websockets |

####  ホスティングサービス

- Arukas
- さくらのVPS

※ArukasのエンドポイントはSSLを要求するが，SPRINTのテストがwsを要求するためVPS上にも同じコードを展開した．

## 独自コマンドの実装

```
===== Plugins =====

8 plugins are installed.

* todo [add|delete|list] [args...]
  - add [title] [description...] : Add task with the title
  - delete [title] : Delete task which have the title
  - list : Print all tasks

ex)
  > todo add foo bar
  todo added

  > todo delete foo
  todo deleted

  > todo list
  foo bar


* tz [timezone]
Convert current time to specific timezone.

ex)
  > tz UTC
  UTC : 2016-12-02T14:34:22.510503+00:00

  > tz Asia/Tokyo
  Asia/Tokyo : 2016-12-02T23:34:47.996641+09:00


* weather [location]
Print current weather observations and forecast

ex)
> weather Tokyo
2016-12-02 02:00:00+00 Clear
2016-12-03 02:00:00+00 Clear
2016-12-04 02:00:00+00 Clear
2016-12-05 02:00:00+00 Rain
2016-12-06 02:00:00+00 Rain
2016-12-07 02:00:00+00 Clear
2016-12-08 02:00:00+00 Rain


* hash [string1] [string2]
Convert from ASCII string to hash string.

ex)
  > hash a b
  c3


* ping
Just say "pong".

ex)
  > ping
  pong


* help
Print all installed plugin with help string.

* echo [text...]
echo says a line of text.

ex)
  > echo hoge
  hoge


* gengo [yyyy/mm/dd]
Convert from string to Japanese Gengo.
If string is not given, use current time.

ex)
  > gengo
  平成28年12月2日

  > gengo 2000/01/01
  平成12年1月1日
```

## 旧subotからの変更点

- プラグインにKVSを提供
    - 環境変数にREDIS_HOSTとREDIS_PORTが存在する場合，Redisを使用する．
    - Redisを使用できない場合，dictを使用する．
        - ただし，永続化しない．
