#! /usr/bin/env python3

from datetime import datetime, timedelta
from pathlib import Path
import numpy as np
import pandas as pd
import xarray as xr
import io
import warnings
import logging

from ...util import read_as_str


def get_url(time: datetime) -> str:

    return (
        "https://ds.data.jma.go.jp/goos/data/pub/JMA-product/him_sst_pac_D"
        f"/{time:%Y}/him_sst_pac_D{time:%Y%m%d}.txt"
    )


def get_save_fpath(time: datetime, data_dir: Path) -> Path:

    return data_dir / Path(
        (f"HIMSST/Daily/{time:%Y}/{time:%Y%m}/" f"him_sst_pac_D{time:%Y%m%d}.nc")
    )


def himsst_download(
    start_time: datetime,
    end_time: datetime,
    data_dir: Path,
    exist_skip: bool = False,
) -> None:

    time_list = []
    time = start_time
    while time <= end_time:
        time_list.append(time)
        time += timedelta(days=1)

    for time in time_list:

        url = get_url(time)
        save_fpath = get_save_fpath(time, data_dir)
        save_fpath.parent.mkdir(parents=True, exist_ok=True)

        text = read_as_str(url)
        if text is None:
            warnings.warn(f'Error while downloading "{url}".')
        else:
            f = io.StringIO(text)
            with f as file:
                header = file.readline().strip()
                year = int(header[:4])
                month = int(header[4:8])

                df = pd.read_fwf(f, widths=[3] * 800, nrows=600, header=None)

                arr = (
                    df.apply(pd.to_numeric, errors="coerce")
                    .to_numpy(dtype=float)
                    .copy()
                )
                ice = (arr == 888).astype(int)
                land = (arr == 999).astype(int)
                arr[arr == 888] = np.nan
                arr[arr == 999] = np.nan
                arr *= 0.1
                lat = np.arange(59.95, 0.05 - 0.1, -0.1)
                lon = np.arange(100.05, 179.95 + 0.1, 0.1)

                ds = xr.Dataset(
                    {
                        "sst": (("lat", "lon"), arr),
                        "seaice": (("lat", "lon"), ice),
                        "land": (("lat", "lon"), land),
                    },
                    coords={
                        "lat": lat,
                        "lon": lon,
                    },
                    attrs={"ORIGINAL_URL": url},
                )

                ds.to_netcdf(save_fpath)
                logging.info(f"{url} =(file conversion)=> {save_fpath}")
