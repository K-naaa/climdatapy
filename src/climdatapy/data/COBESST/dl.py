#! /usr/bin/env python3

from datetime import datetime
from pathlib import Path
import numpy as np
import pandas as pd
import xarray as xr
import io
import logging
import warnings

from ...util import read_as_str


def get_url(year: int, month: int) -> str:

    return (
        "https://ds.data.jma.go.jp/goos/data/pub/JMA-product/"
        f"cobe2_sst_glb_M/{year:04}/cobe2_sst_glb_M{year:04}{month:02}.txt"
    )


def get_save_fpath(year: int, month: int, data_dir: Path) -> Path:

    return data_dir / Path(
        (f"COBESST2/Monthly/{year:04}/cobe2_sst_glb_M{year:04}{month:02}.nc")
    )


def cobesst_download(
    start_time: datetime, end_time: datetime, data_dir: Path, exist_skip: bool = False
) -> None:

    if start_time.year == end_time.year:
        year_month = [
            (start_time.year, month)
            for month in range(start_time.month, end_time.month + 1)
        ]
    else:
        year_month = [(start_time.year, month) for month in range(start_time.month, 13)]
        for year in range(start_time.year + 1, end_time.year):
            year_month += [(year, month) for month in range(1, 13)]
        year_month += [(end_time.year, month) for month in range(1, end_time.month + 1)]

    for year, month in year_month:

        url = get_url(year, month)
        save_fpath = get_save_fpath(year, month, data_dir)
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

                df = pd.read_fwf(f, widths=[3] * 360, nrows=180, header=None)
                arr = (
                    df.apply(pd.to_numeric, errors="coerce")
                    .to_numpy(dtype=float)
                    .copy()
                )
                arr[arr == 999] = np.nan
                arr *= 0.1
                lat = np.arange(89.5, -89.5 - 1.0, -1.0)

                lon = np.arange(0.5, 359.5 + 1.0, 1.0)

                ds = xr.DataArray(
                    arr,
                    dims=("lat", "lon"),
                    coords={"lat": lat, "lon": lon},
                    name="SST",
                    attrs={"ORIGINAL_URL": url},
                )

                ds.to_netcdf(save_fpath)
                logging.info(f"{url} =(file conversion)=> {save_fpath}")
