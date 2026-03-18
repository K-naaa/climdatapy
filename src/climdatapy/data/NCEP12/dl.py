#! /usr/bin/env python3

from datetime import datetime
from pathlib import Path

from ...util import download


prs_vars_re1 = [
    "air",
    "hgt",
    "omega",
    "rhum",
    "shum",
    "uwnd",
    "vwnd",
]
srf_vars_re1 = [
    "air.sig995",
    "omega.sig995",
    "pottmp.sig995",
    "pres.sfc",
    "pr_wtr.eatm",
    "rhum.sig995",
    "slp",
    "uwnd.sig995",
    "vwnd.sig995",
]
prs_vars_re2 = [
    "air",
    "hgt",
    "omega",
    "rhum",
    "uwnd",
    "vwnd",
]
srf_vars_re2 = [
    "mslp",
    "pr_wtr.eatm",
    "pres.sfc",
]


def get_filename(
    year: int,
    stats_type: str,
    var: str,
    **kwargs,
) -> str:

    if stats_type in ["6hourly", "daily"]:
        filename = f"{var}.{year:04}.nc"
    elif stats_type == "monthly":
        filename = f"{var}.mon.mean.nc"

    return filename


def get_url(
    dataset_name: str, year: int, stats_type: str, data_kind: str, var: str
) -> str:

    BASE_URL = "https://database.rish.kyoto-u.ac.jp/arch/ncep/data/"

    url = BASE_URL

    if dataset_name == "Reanalysis1":
        url += "ncep.reanalysis"
    elif dataset_name == "Reanalysis2":
        url += "ncep.reanalysis2"

    if stats_type == "6hourly":
        url += "/"
    elif stats_type == "daily":
        url += ".dailyavgs/"
    elif stats_type == "monthly":
        url += ".derived/"
    else:
        raise

    if data_kind == "pressure":
        url += "pressure/"
    elif data_kind == "surface":
        url += "surface/"
    else:
        raise

    url += get_filename(year, stats_type, var)

    return url


def get_save_fpath(
    dataset_name: str,
    year: int,
    stats_type: str,
    data_kind: str,
    var: str,
    base_dir: Path,
) -> Path:

    return Path(
        f"{base_dir}/NCEP_{dataset_name}/{stats_type}/{data_kind}/{var}"
        f"/{get_filename(year,stats_type,var)}"
    )


def ncep12_download(
    start_time: datetime,
    end_time: datetime,
    dataset_name: str,
    stats_type: str,
    data_kind: str,
    var: str,
    base_dir: Path,
    exist_skip: bool = False,
) -> None:

    for year in range(start_time.year, end_time.year + 1):

        url = get_url(dataset_name, year, stats_type, data_kind, var)
        save_fpath = get_save_fpath(
            dataset_name, year, stats_type, data_kind, var, base_dir
        )

        download(
            url,
            save_fpath,
            download_method="util_url_noauth",
            exist_skip=exist_skip,
        )
