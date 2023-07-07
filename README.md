## フォルダの説明
sample フォルダ: スクショのデータ，ラベル(labels.txt)，OCRの書き起こし，整形した書き起こしを保存  
pickle フォルダ：データセットをpickleにして保存．現状は整形した文字列をデータに入れている

## スクリプトの説明
run.sh: sampleフォルダにあるpngファイルをOCRする(tesseractを使用)  

clean_ocr.py: OCRしたテキストをChatGPTを用いて整形  

create_dataset.py: 整形した文字列データ(X)とアノテーションラベル(y)をデータセットとして作成．各画像のラベルをtrain, val, testで6:2:2で分割

data_loader.py: train, val, testで，整形した文字列とラベルのペアをバッチで取り出す

## アノテーションデータの追加方法
sampleフォルダ内に新しいフォルダを作って(ex. 07)，その中にpng形式のスクショと，labels.txtというtxtファイルを作ってそのなかに，改行区切りでラベルを付けてください

## 動かし方
0. Linux上に[tesseract](https://github.com/tesseract-ocr/tesseract)
(OCRモデル)のインストール

1. `run.sh` でsampleフォルダ内のpngファイルをOCRして，各フォルダのraw_transcription.txtに保存
2. `clean_ocr.py`内で`API_KEY`変数にGPT-4のAPIを設定.
3. `clean_ocr.py'`内の`prompt`変数にchatgptに対するプロンプトを記入
4. `python clean_ocr.py`でOCRを整形して，cleaned_ocr.txtに保存
5. `python create_dataset.py`でchatgptのプロンプトに基づき，OCRを整形し，datasetを作成
6. `python dataloader.py`で，整形したテキストとラベルのペアをバッチで取り出す