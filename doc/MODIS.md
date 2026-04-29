# MODIS

## Source
[EATHDATA](https://ladsweb.modaps.eosdis.nasa.gov/archive/allData/62/MCD06COSP_D3_MODIS/)で公開されているnetCDFデータをダウンロードする。

## ```download_kw```
指定する必要はない。このスクリプトでは雲画像のみのダウンロードのため。

## ```.climdatarc```
以下の変数を設定する。

|変数名||
|---|---|
|```MODISUsername```|EATHDATAのユーザ名|
|```MODISPassward```|EATHDATAのパスワード|