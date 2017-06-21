

# 前提

* gRPCを用いて `api.proto` ファイルからInterfaceを生成し、Serverを実装してください
	* 実装に利用する言語は下記より選択してください
		* Go
		* Java
		* Ruby
		* Python
		* PHP
		* JavaScript(Node.js)
	* Ref. http://www.grpc.io/
* 公開されているオープンソースライセンスのライブラリなど利用できます

# 概要

* CRUD機能を提供するItem APIサーバの実装

## 提供ファイル

* software-engineer-course.md
* docker-compose.yml
* api.proto

# サーバの仕様

* サーバのポート番号は3000を指定してください
* datastoreは `Redis` or `MySQL` を選択してください
* 提供している `docker-compose.yml` などを利用して環境を構築してください

## ListItemの仕様

* `ListItemRequest.limit` で指定された件数分の `Item` を返却してください
* `ListItemRequest.page` と `ListItemRequest.limit` を利用してpaginationを実装してください

## GetItemの仕様

* `GetItemRequest.id` と一致する `Item` を返却してください
* requestが成功するごとに `GetItemRequest.id` と一致する `Item` の `Item.pv` をincrementしてください
	* responseの `Item.pv` の値はincrementした値を返却して下さい

## AddItemの仕様

* `AddItemRequest.item` をdatastoreに保存してください
* 成功した場合は保存した `Item` を返却してください

## UpdateItemの仕様

* 既存の対象の `Item` を `UpdateItemRequest.item` に更新してください
* 成功した場合は更新した `Item` を返却してください

## DeleteItemの仕様

* `DeleteItemRequest.id` と一致する `Item` を削除してください

# 提出方法

* GitHubのGist機能を利用し、作成したURLをご提出ください。その際は必ず **secret gist** として作成してください

## 提出ファイル

* README.md
	* 手順や補足などあれば記入してください
* docker-compose.yml
* その他実装したソースコード一式