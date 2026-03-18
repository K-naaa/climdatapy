# 1. climdatapy
<p>
<img src="https://img.shields.io/github/license/sotomita/bsod">
<img src="https://img.shields.io/badge/-Python-gray.svg?logo=Python">
</p>

[![Publish to PyPI](https://github.com/sotomita/climdatapy/actions/workflows/publish.yml/badge.svg)](https://github.com/sotomita/climdatapy/actions/workflows/publish.yml)

気象・海洋のデータセットをダウンロードするCLI/Pythonパッケージ。
- [1. climdatapy](#1-climdatapy)
- [2. Installation](#2-installation)
- [3. Usage](#3-usage)
  - [3.1. CLI](#31-cli)
    - [3.1.1. ダウンロード可能データセットを表示](#311-ダウンロード可能データセットを表示)
    - [3.1.2. データセットをダウンロード](#312-データセットをダウンロード)
    - [3.1.3. 最新データをダウンロード](#313-最新データをダウンロード)
  - [3.2. Pythonモジュール](#32-pythonモジュール)
    - [3.2.1. ```dowload```メソッド](#321-dowloadメソッド)
    - [3.2.2. ```download_all```メソッド](#322-download_allメソッド)
    - [3.2.3. ```update```メソッド](#323-updateメソッド)
    - [3.2.4. ```update_all```メソッド](#324-update_allメソッド)
  - [3.3. 対応データセット](#33-対応データセット)
  - [3.4. サンプルスクリプト](#34-サンプルスクリプト)
- [4. Author](#4-author)


# 2. Installation
Python 3.11以上が必要。

```pip```コマンドを使い、[PyPI](https://pypi.org/project/climdatapy/)からインストールする。
```bash
$ pip install climdatapy
```

# 3. Usage
## 3.1. CLI
```climdata```コマンドでデータセットを管理する。
### 3.1.1. ダウンロード可能データセットを表示
```$ climdata list```
### 3.1.2. データセットをダウンロード
(例) 2024年1月1日から1月2日までのJRA3Qデータをダウンロードする。
```
$ climdata download JRA3Q --start_time 2024-01-01 --end_time 2024-01-02 --out ./JRA3Q --logfile jra3q.log --skip_existing
```
引数の説明は```-h```オプションで確認できる。
```
$ climdata download -h
usage: climdata download [-h] --start_time START_TIME --end_time END_TIME [--out OUT] [--logfile LOGFILE] [--skip_existing] dataset

Download files for a specified dataset and time range.

positional arguments:
  dataset               dataset name

options:
  -h, --help            show this help message and exit
  --start_time START_TIME
                        start date (YYYY-MM-DD)
  --end_time END_TIME   end date (YYYY-MM-DD)
  --out OUT             output directory
  --logfile LOGFILE     logfile path
  --skip_existing       set for ignore existing files
```

### 3.1.3. 最新データをダウンロード
(例) 公開されている最新のJRA3Qデータをダウンロードする。
```
$ climdata update JRA3Q --out ./JRA3Q --logfile jra3q.log --skip_existing
```
引数の説明は```-h```オプションで確認できる。
```
$ climdata update -h
usage: climdata update [-h] [--out OUT] [--logfile LOGFILE] [--skip_existing] dataset

positional arguments:
  dataset            dataset name

options:
  -h, --help         show this help message and exit
  --out OUT          output directory
  --logfile LOGFILE  logfile path
  --skip_existing       set for ignore existing files
```

## 3.2. Pythonモジュール
各データセットは、抽象基底クラス```climdata.util.Dataset```を継承したデータセット管理クラス(以下、管理クラス)を持つ。

```climdatapy.get_manager```関数で管理クラスを取得する。
```
import climdatapy

manager = climdatapy.get_manager("JRA3Q")
```
### 3.2.1. ```dowload```メソッド
任意の時間の範囲、変数などを選択し、ダウンロードする。

(例)
```
start_time = datetime(2025, 1, 1, 0)
end_time = datetime(2025, 1, 1, 6)
download_kw = {
    "stats_type": ["all"],
    "data_kind": ["all"],
    "near_realtime": ["all"],
    "stats_type": ["all"],
    "std": ["true"],
    "var": ["all"],
}

data_dir = Path("./data_new")
log_file_path = Path("./jra3q.log")

manager.download(
    start_time,
    end_time,
    download_kw,
    data_dir,
    log_file_path,
    exist_ok=True,
)
```
```download_kw```はデータセット固有の情報を辞書型で格納する。

詳細は各データセットの説明([```doc```](./doc/))を参照。

### 3.2.2. ```download_all```メソッド
指定できる最大限の```download_kw```を```download```メソッドに与えるwrapper。

### 3.2.3. ```update```メソッド
取得できる最新の時刻のデータをダウンロードする。

(例)
```
manager.update(
    download_kw,
    data_dir,
    log_file_path,
    exist_ok=True,
)
```

### 3.2.4. ```update_all```メソッド
指定できる最大限の```download_kw```を```update```メソッドに与えるwrapper。

## 3.3. 対応データセット
||source||
|---|---|---|
|JRA3Q|[NCAR GDEX](https://gdex.ucar.edu/)|[詳細](./doc/JRA3Q.md)|
|NCEP Reanalysis1|[京大生存圏DB](https://database.rish.kyoto-u.ac.jp/arch/ncep/)|[詳細](./doc/NCEP1.md)|
|NCEP Reanalysis2|[京大生存圏DB](https://database.rish.kyoto-u.ac.jp/arch/ncep/)|[詳細](./doc/NCEP2.md)|
|OISST|[NOAA NCEI](https://www.ncei.noaa.gov/products/optimum-interpolation-sst)|[詳細](./doc/OISST.md)|
|COBESST|[JMA NEAR-GOOS](https://ds.data.jma.go.jp/goos/data/rrtdb/jma-pro/cobe2_sst_glb_M.html)|[詳細](./doc/COBESST.md)|
|HIMSST|[JMA NEAR-GOOS](https://ds.data.jma.go.jp/goos/data/rrtdb/jma-pro/him_sst_pac_D.html)|[詳細](./doc/HIMSST.md)|

各データ使用の際の引用や謝辞等の規定はsourceを参照してください。


## 3.4. サンプルスクリプト
|||
|---|---|
|[```sample/download_JRA3Q.py```](./sample/download_JRA3Q.py)|JRA3Qのダウンロード|
|[```sample/update_JRA3Q.py```](./sample/update_JRA3Q.py)|JRA3Qの更新|
# 4. Author
- [So Tomita](https://github.com/sotomita)