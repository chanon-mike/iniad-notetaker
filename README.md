# INIAD Note Taker

INIAD MOOCs システムのメモを取るプロセスを Web スクレイピングで自動化する

### 見つけたバグ・問題

[ ] スライドのアニメーションにより、同じ内容が複数ページにスクレイプされる。

### インストール方法

このレポシトリーをクローン・フォーク・ダウンロードをしてください。

```
$ git clone git@github.com:chanon-mike/iniad-notetaker.git
$ cd iniad-notetaker
```

環境を作って、必要あなライブラリーをインストールしてください。(Windows の方は WSL の Chrome や Chromedriver のインストールが必要のため、Windows Power Shell などをおススメします)

```
$ python -m venv venv
$ .\venv\Scripts\activate
$ pip install -r requirements.txt
```

ローカル環境での`.env.example`のファイル内容を自分のアカウントに変更し、`.env`にファイル名を変更してください。

```
USERNAME = MOOCsのユーザーID
PASSWORD = MOOCsのパスワード
EMAIL = iniad.orgのメールアドレス
```

### 使用方法

```
$ python main.py
```

MOOCs スライドが載っているサイトの URL を入力して、テキスト情報が output フォルダーに保存されます。

### Note

本ソフトウェアは、東洋大学及び東洋大学情報連携学部の公式ソフトウェア又は公式サービスとして公認、公開、頒布等しているものではありません。

本サービスにて提供する情報の正確性・妥当性につきましては細心の注意を払っておりますが、当作者はその保証をするものではありません。本サービスの利用によって利用者や第三者等にネットワーク障害等による損害、データの損失その他あらゆる不具合、不都合が生じた場合について、裁判所またはそれに準ずる機関で当作者の重過失が認められた場合を除き、当作者では一切の責任を負いません。

### License

本ソフトウェアは、MIT ライセンスの下で提供されています。
