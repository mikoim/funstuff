## STEP1. デプロイ情報

 - https://subot.arukascloud.io/
 - （´・ω・） ｽ → GitHub → CircleCI → Docker Hub → Arukas

## STEP2. 必須機能の実装

特記することはありません．

## STEP3. 独自コマンドの実装

 - hash string1 string2 : 基本問題のハッシュを移植したもの．
 - help : インストールされたプラグインとその説明を列挙する．
 - gengo (yyyy/mm/dd) : 忘れがちな元号を表示．日付を指定しない場合は今日の日付をもとに表示する．
 - weather location : OpenWeatherMapの天気予報を表示する．
 - tz timezone : 指定したタイムゾーンに現在時刻を変換する．

```
bot help
===== Plugins =====

weather location
Print current weather observations and forecast

ping
Just say "pong".

help
Print all installed plugin with help string.

hash string1 string2
Convert from ASCII string to hash string.

gengo (yyyy/mm/dd)
Convert from string to Japanese Gengo.
If string is not given, use current time.

todo (add|delete|list) args...
 - add title description... : Add task
 - delete title : Delete task which have the title
 - list : Print all tasks

tz timezone
Convert current time to specific timezone.

7 plugins are installed.
```

## 今回の開発に使用した技術

 - Python 3.5.x
    - websockets 3.1 : https://pypi.python.org/pypi/websockets
    - rfGengou 0.3 : https://github.com/hATrayflood/rfGengou
    - redis 2.10.5 : https://github.com/andymccurdy/redis-py
    - PyOWM 2.3.1 : https://github.com/csparpa/pyowm
    - pytz 2016.4 : http://pytz.sourceforge.net

Thank contributors for Python and great modules!!!

## 創意工夫点、アピールポイントなど

### Plugins

importlib万歳

### Docker

本当はGAEにデプロイするつもりだったのですが，
WebSocketをうまく通せなかったこと（かと言って，Channel APIを使うわけにもいかず），
処理系のバージョンが古いこと，の2点から「好き勝手にコンテナ作って，適当に上げれば（ｒｙ」に至りました．

つまり何が言いたいのかというと…Dockerは甘え

Dockerも好きですよ，もちろん．

## ひと言コメント

何故もっとはやくから取り組まなかったのか…

なんにしてもPythonが（*´・ω・） ｽｷ!
