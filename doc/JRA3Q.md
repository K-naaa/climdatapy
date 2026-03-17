# JRA3Q
## Source
NCAR GDEXにて公開されている以下のDatasetsからダウンロードする。
||dataset number|Format|```near_realtime```|
|---|:---:|:---:|:---:|
|[Japanese Reanalysis for Three Quarters of a Century (JRA-3Q)](https://gdex.ucar.edu/datasets/d640000/)|d640000|NetCDF4|"false"|
|[Near Real-Time Japanese Reanalysis for Three Quarters of a Century (JRA-3Q)](https://gdex.ucar.edu/datasets/d640001/)|d640001|GRIB2|"true"|
|[Japanese Reanalysis for Three Quarters of a Century (JRA-3Q) Monthly Statistics](https://gdex.ucar.edu/datasets/d640002/)|d640002|NetCDF4|"false"|
|[Near real-time monthly mean Japanese Reanalysis for Three Quarters of a Century (JRA-3Q)](https://gdex.ucar.edu/datasets/d640003/)|d640003|GRIB2|"true"|
|[Japanese Reanalysis for Three Quarters of a Century (JRA-3Q) Diurnal Statistics](https://gdex.ucar.edu/datasets/d640004/)|d640004|NetCDF4|"false"|
|[Near real-time monthly diurnal Japanese Reanalysis for Three Quarters of a Century (JRA-3Q)](https://gdex.ucar.edu/datasets/d640005/)|d640005|GRIB2|"true"|


## ```download_kw```

|key|description|values|default values in ```download_all```|
|:---:|:---|:---|:---:|
|```stats_type```|統計処理の種別|"instant":瞬間値,   "monthly":月平均,  "diurnal":時別月別平均,  "all": 上記全て|"all"|
|```data_kind```|予報値/解析値、解像度などの種別|"anl_isentrop125","anl_land125", "anl_p125", "anl_snow125", "anl_surf125","all"|"all"|
|```near_realtime```|"true":準リアルタイムのファイルを含める  "false":全期間のファイルのみ|"true","false","all"|"all"|
|```std```|"true"("false"): 標準偏差のファイルを含める(含めない)|"true","false"|"true"|
|```var```|変数名|(省略)|"all"|

