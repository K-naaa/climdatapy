# NCEP1

## Source
[京大生存圏データベース](https://www.rish.kyoto-u.ac.jp/dbhs/)にて公開されているNetCDFファイルをダウンロードする。

## ```download_kw```
|key|description|values|default values in ```download_all```|
|:---:|:---|:---|:---:|
|```dataset_name```|データセット名|"Reanalysis1"|"Reanalysis1"|
|```data_kind```|高度の種別|"pressure":気圧面、"surface":地表面,"all":上記全て|"all"|
|```stats_type```|統計処理の種別|"6hourly":6時間毎の瞬間値,"daily":日平均,"monthly":月平均,"all":上記全て|"all"|
|```var```|変数名|(省略)|"all"|
