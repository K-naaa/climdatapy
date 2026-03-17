#! /usr/bin/env python3

"""
JRA3Qをダウンロードするサンプルスクリプト
"""


from datetime import datetime
from pathlib import Path

import climdatapy

print(f"climdatapy version = {climdatapy.__version__}")

# JRA3Q管理クラスを取得
manager = climdatapy.get_manager("JRA3Q")

# 2025年1-5月のanl_surf125をダウンロード
manager.download(
    start_time=datetime(2020, 1, 1, 0),
    end_time=datetime(2020, 5, 31, 18),
    download_kw={
        "stats_type": ["instant"],
        "data_kind": ["anl_suf125"],
        "near_realtime": ["all"],
        "stats_type": ["all"],
        "std": ["true"],
        "var": ["all"],
    },
    data_dir=Path("./data"),
    log_file_path=Path("./donload_jra3q.log"),
    exist_ok=True,
)

# または、download_allメソッドで、ダウンロード可能なすべてのファイルを取得する。
"""manager.download_all(
    start_time=datetime(2020, 1, 1, 0),
    end_time=datetime(2020, 5, 31, 18),
    data_dir=Path("./data"),
    log_file_path=Path("./donload_jra3q.log"),
    exist_ok=True,
)"""
