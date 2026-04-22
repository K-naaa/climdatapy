#! /usr/bin/env python3

"""
MODISをダウンロードするサンプルスクリプト
"""

from datetime import datetime
from pathlib import Path

import climdatapy

# MODIS管理クラスを取得
manager = climdatapy.get_manager("MODIS")

manager.download(
    start_time=datetime(2022, 12, 1),  
    end_time=datetime(2026, 3, 29),
    data_dir=Path("/DATA/DATA/PUBLIC_DATA/MODIS/MCD06COSP_D3_MODIS"),
    exist_ok=True,
)