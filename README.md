# climdatapy
<p>
<img src="https://img.shields.io/github/license/sotomita/bsod">
<img src="https://img.shields.io/badge/-Python-gray.svg?logo=Python">
</p>
気象・海洋のデータセットをダウンロードするCLI/Pythonパッケージ。

## Installation
Python 3.14以上が必要。

```pip```コマンドを使い、PyPIからインストールする。
```bash
$ pip install climdatapy
```

## Usage
### CLI
```climdata```コマンドでデータセットを管理します。
#### ダウンロード可能データセットを表示
```climdata list```
#### データセットをダウンロード
(例) 2024年1月1日から1月2日までのJRA3Qデータをダウンロードする。
```
$ climdata download JRA3Q --start_time 2024-01-01 --end_time 2024-01-02 --out ./JRA3Q --logfile jra3q.log
```
引数の説明は```-h```オプションで確認できる。
```
$ climdata download -h
usage: climdata download [-h] --start_time START_TIME --end_time END_TIME [--out OUT] [--logfile LOGFILE] dataset

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
```

#### 最新データをダウンロード
(例) 公開されている最新のJRA3Qデータをダウンロードする。
```
$ climdata update JRA3Q --out ./JRA3Q --logfile jra3q.log
```
引数の説明は```-h```オプションで確認できる。
```
$ climdata update -h
usage: climdata update [-h] [--out OUT] [--logfile LOGFILE] dataset

positional arguments:
  dataset            dataset name

options:
  -h, --help         show this help message and exit
  --out OUT          output directory
  --logfile LOGFILE  logfile path
```

### Pythonモジュール
各データセットは、抽象基底クラス```climdata.util.Dataset```を継承したデータセット管理クラス(以下、管理クラス)を持つ。

```climdatapy.get_manager```関数で管理クラスを取得する。
```
import climdatapy

manager = climdatapy.get_manager("JRA3Q")
```
#### ```dowload```メソッド
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
```download_kw```はデータセット固有の設定すべき情報を辞書型で確認する。

#### ```download_all```メソッド
指定できる最大限の```download_kw```を```download```メソッドに与えるwrapper。

#### ```update```メソッド
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

#### ```update_all```メソッド
指定できる最大限の```download_kw```を```update```メソッドに与えるwrapper。

### 対応データセット
- JRA3Q

## Author
- [So Tomita](https://github.com/sotomita)