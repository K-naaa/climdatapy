#! /usr/bin/env python3

"""
直近に公開されたMODISをダウンロードするサンプルスクリプト
"""


from datetime import datetime, timedelta
from pathlib import Path

import climdatapy

print(f"climdatapy version = {climdatapy.__version__}")

# MODIS管理クラスを取得
manager = climdatapy.get_manager("MODIS")

# 更新が少し遅れていそうなので、余裕を持つ
end_time = datetime.now() - timedelta(days=8)

# 直近7日だけ取得
start_time = end_time - timedelta(days=7)

manager.download(
    start_time=start_time,
    end_time=end_time,
    data_dir=Path("/DATA/DATA/PUBLIC_DATA/MODIS/MCD06COSP_D3_MODIS"),
    exist_ok=True,  # 既存データはスキップ
)