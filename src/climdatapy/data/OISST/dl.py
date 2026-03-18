#! /usr/bin/env python3

from datetime import datetime, timedelta
from pathlib import Path

from ...util import download


def get_filename(time: datetime, **kwargs) -> str:

    return f"oisst-avhrr-v02r01.{time:%Y%m%d}.nc"


def get_url(time: datetime, **kwargs) -> str:

    return (
        "https://www.ncei.noaa.gov/data/sea-surface-temperature-optimum-interpolation/v2.1/access/avhrr/"
        f"{time:%Y%m}/{get_filename(time)}"
    )


def get_save_fpath(time: datetime, base_dir: Path) -> Path:

    return Path(f"{base_dir}/OISST/v2.1/{time:%Y}/{time:%Y%m}/{get_filename(time)}")


def oisst_download(
    start_time: datetime, end_time: datetime, base_dir: Path, exist_skip: bool, **kwargs
) -> None:

    time = start_time
    while time <= end_time:
        url = get_url(time)
        save_fpath = get_save_fpath(time, base_dir)
        download(
            url,
            save_fpath,
            download_method="util_url_noauth",
            exist_skip=exist_skip,
        )
        time += timedelta(days=1)
