# ペーパー業務管理ツール (MVP)

このプロジェクトは、データ入力作業と紙書類の取り扱いをローカル環境で管理する最小構成のサンプルです。Python 製バックエンドは Google Cloud Functions Framework を用い、フロントエンドには React を使用しています。

## 必要要件
- Python 3.9 以上
- Node.js 16 以上
- Docker (Firestore エミュレータ用)

## Docker の使い方
1. Docker Desktop もしくは Docker Engine をインストールし、`docker --version` で確認します。Docker デーモンが起動していることを `docker info` で確かめてください。起動していないと `open //./pipe/dockerDesktopLinuxEngine: The system cannot find the file specified` のようなエラーが出ます。
2. エミュレータ用イメージを取得します (初回は自動取得されるため省略可)。
   ```bash
docker pull google/cloud-sdk:emulators
   ```
3. Firestore エミュレータを起動します (このターミナルは開いたままにします)。
   - **Linux/macOS**
     ```bash
docker run --rm -it -p 8081:8080 google/cloud-sdk:emulators \
       gcloud beta emulators firestore start --host-port=0.0.0.0:8080
     ```
   - **Windows (cmd.exe)**
     ```cmd
docker run --rm -it -p 8081:8080 google/cloud-sdk:emulators ^
       gcloud beta emulators firestore start --host-port=0.0.0.0:8080
     ```
     `^` の後ろにスペースを入れないよう注意してください。`Ctrl+C` で停止するとコンテナは自動的に削除されます。
4. **任意**: Cloud Storage エミュレータを起動する場合
   - **Linux/macOS**
     ```bash
docker run --rm -it -p 4443:4443 google/cloud-sdk:emulators \
       gcloud beta emulators storage start --host-port=0.0.0.0:4443
     ```
   - **Windows (cmd.exe)**
     ```cmd
docker run --rm -it -p 4443:4443 google/cloud-sdk:emulators ^
       gcloud beta emulators storage start --host-port=0.0.0.0:4443
     ```
     こちらも `^` の後にスペースを入れないでください。バックエンド実行時には `STORAGE_EMULATOR_HOST=localhost:4443` を設定します。

## ローカル環境での実行手順
1. 上記の手順で Firestore エミュレータ (必要に応じて Storage エミュレータ) を起動し、環境変数 `FIRESTORE_EMULATOR_HOST` (および `STORAGE_EMULATOR_HOST`) を設定します。
2. **バックエンドのセットアップ**
   ```bash
   cd backend
   pip install -r requirements.txt
   export GOOGLE_CLOUD_PROJECT=local-project
   export BUCKET_NAME=receipt-images
   export FIRESTORE_EMULATOR_HOST=localhost:8081
   export STORAGE_EMULATOR_HOST=localhost:4443
   functions-framework --target=app
   ```
   Windows の場合は `export` ではなく `set` または PowerShell 用の `$env:` を使用します。
3. **フロントエンドの起動**
   ```bash
   cd ../frontend
   npm install
   REACT_APP_API_BASE=http://localhost:8080 npm start
   ```
   Windows では `set REACT_APP_API_BASE=http://localhost:8080` または `$env:REACT_APP_API_BASE='http://localhost:8080'` を使用します。ブラウザで <http://localhost:3000> を開くとアプリが表示されます。
4. **API の確認** (例)
   ```bash
   curl http://localhost:8080/receipts
   ```

## Docker Compose を使う場合
`docker-compose up` を実行すると、Firestore エミュレータ、Cloud Storage エミュレータ、バックエンドがまとめて起動します。ポートはそれぞれ 8081、4443、8080 です。`docker-compose down` で停止します。v2 では `version` フィールドは無視されるため `docker-compose.yml` から削除してあります。

ポートが既に使用されている場合は `Bind for 0.0.0.0:8081 failed: port is already allocated` のようなエラーが出ます。別プロセスを停止するか `docker-compose.yml` のポート設定を変更してください。

Firestore エミュレータに保存されたデータやアップロードした画像はコンテナの停止で消えるため、必要に応じてバックアップを取ってください。
