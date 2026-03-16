#! /usr/bin/env python3

from datetime import datetime
from pathlib import Path

import climdatapy

manager = climdatapy.get_manager("JRA3Q")

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

"""manager.download(
    start_time,
    end_time,
    download_kw,
    data_dir,
    log_file_path,
    exist_ok=True,
)"""

"""manager.download_all(
    start_time,
    end_time,
    data_dir,
    log_file_path,
    exist_ok=True,
)"""

manager.update(
    download_kw,
    data_dir,
    log_file_path,
    exist_ok=True,
)
