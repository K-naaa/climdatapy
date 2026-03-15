#! /usr/bin/env python3

from datetime import datetime, timedelta
from pathlib import Path

from .param import code_dict
from ...util import download


def get_tail_time(
    year: int, month: int, dt: timedelta = timedelta(hours=6), **kwargs
) -> datetime:

    tail_time = datetime(year, month + 1, 1) if month < 12 else datetime(year + 1, 1, 1)
    return tail_time - dt


def __get_file_name(
    stats_type: str,
    data_kind: str,
    var: str,
    year: int,
    month: int,
    std: bool = False,
    **kwargs,
) -> str:

    if stats_type not in ["instant", "monthly", "diurnal"]:
        raise ValueError('stats_type must be one of "instant","monthly","diurnal"')

    if data_kind == "anl_snow125":
        if stats_type != "instant":
            raise RuntimeError("anl_snow125 is only supported in instant values.")
        start_date = datetime(year, month, 1, 18)
    else:
        start_date = datetime(year, month, 1, 0)
    tail_date = get_tail_time(year, month, **kwargs)

    mn_or_std = "std" if std else "mn"
    code = code_dict[data_kind][var]

    if stats_type == "instant":
        fname = (
            f"jra3q.{data_kind}.{code[0]}_{code[1]}_{code[2]}.{var}-an-ll125"
            f".{start_date.strftime('%Y%m%d%H')}_{tail_date.strftime('%Y%m%d%H')}.nc"
        )
    elif stats_type == "monthly":
        fname = (
            f"jra3q-ms-{mn_or_std}.{data_kind}.{code[0]}_{code[1]}_{code[2]}.{var}-an-ll125-{mn_or_std}"
            f".{start_date.strftime('%Y%m%d%H')}_{tail_date.strftime('%Y%m%d%H')}.nc"
        )
    elif stats_type == "diurnal":
        fname = (
            f"jra3q-ds-{mn_or_std}.{data_kind}.{code[0]}_{code[1]}_{code[2]}.{var}-an-ll125-{mn_or_std}"
            f".{start_date.strftime('%Y%m%d%H')}_{tail_date.strftime('%Y%m%d%H')}.nc"
        )

    return fname


def __get_file_name_nrtime(
    stats_type: str,
    data_kind: str,
    var: str,
    year: int,
    month: int,
    day: int = 1,
    hour: int = 0,
    std: bool = False,
    **kwargs,
) -> str:

    if data_kind in ["anl_surf125", "anl_land125", "anl_snow125"]:
        __var = ""
    else:
        __var = f"_{var}"

    if data_kind == "anl_snow125":
        if stats_type != "instant":
            raise RuntimeError("anl_snow125 is only supported in instant values.")
        __time = f"{year:04}{month:02}{day:02}18"
    else:
        if stats_type == "instant":
            __time = f"{year:04}{month:02}{day:02}{hour:02}"
        elif stats_type == "monthly":
            __time = f"{year:04}{month:02}"
        elif stats_type == "diurnal":
            __time = f"{year:04}{month:02}_{hour:02}"

    mn_or_std = "_std" if std else ""

    return f"{data_kind}{__var}{mn_or_std}.{__time}"


def get_file_name(
    stats_type: str,
    data_kind: str,
    var: str,
    year: int,
    month: int,
    day: int = 1,
    hour: int = 0,
    std: bool = False,
    near_real_time: bool = False,
    **kwargs,
) -> str:

    if near_real_time:
        fname = __get_file_name_nrtime(
            stats_type, data_kind, var, year, month, day, hour, std, **kwargs
        )
    else:
        fname = __get_file_name(stats_type, data_kind, var, year, month, std, **kwargs)

    return fname


def get_save_fpath(
    base_dir: Path,
    stats_type: str,
    data_kind: str,
    var: str,
    year: int,
    month: int,
    day: int = 1,
    hour: int = 0,
    std: bool = False,
    near_real_time: bool = False,
    **kwargs,
) -> Path:

    fname = get_file_name(
        stats_type,
        data_kind,
        var,
        year,
        month,
        day,
        hour,
        std,
        near_real_time,
        **kwargs,
    )
    if (stats_type == "instant") and (not near_real_time):
        data_no = "d640000"
    elif (stats_type == "instant") and near_real_time:
        data_no = "d640001"
    if (stats_type == "monthly") and (not near_real_time):
        data_no = "d640002"
    if (stats_type == "monthly") and near_real_time:
        data_no = "d640003"
    if (stats_type == "diurnal") and (not near_real_time):
        data_no = "d640004"
    if (stats_type == "diurnal") and near_real_time:
        data_no = "d640005"

    return base_dir / Path(
        f"{data_no}/{data_kind}/{year:04}/{year:04}{month:02}/{fname}"
    )


def get_url(
    stats_type: str,
    data_kind: str,
    var: str,
    year: int,
    month: int,
    day: int = 1,
    hour: int = 0,
    std: bool = False,
    near_real_time: bool = False,
    **kwargs,
) -> str:

    if (stats_type == "instant") and (not near_real_time):
        data_no = "d640000"
    elif (stats_type == "instant") and near_real_time:
        data_no = "d640001"
    if (stats_type == "monthly") and (not near_real_time):
        data_no = "d640002"
    if (stats_type == "monthly") and near_real_time:
        data_no = "d640003"
    if (stats_type == "diurnal") and (not near_real_time):
        data_no = "d640004"
    if (stats_type == "diurnal") and near_real_time:
        data_no = "d640005"

    fname = get_file_name(
        stats_type,
        data_kind,
        var,
        year,
        month,
        day,
        hour,
        std,
        near_real_time,
        **kwargs,
    )

    __base_url = f"https://osdf-director.osg-htc.org/ncar/gdex/{data_no}"
    return f"{__base_url}/{data_kind}/{year:04d}{month:02d}/{fname}"


def get_year_month_list(
    start_year: int,
    start_month: int,
    end_year: int,
    end_month: int,
    **kwargs,
) -> list[tuple[int, int]]:

    year_month_list = []

    for year in range(start_year, end_year + 1):

        if (year == start_year) and (year != end_year):
            months = range(start_month, 13)
        elif (year != start_year) and (year == end_year):
            months = range(1, end_month + 1)
        elif (year == start_year) and (year == end_year):
            months = range(start_month, end_month + 1)

        else:
            months = range(1, 13)

        for month in months:
            year_month_list.append((year, month))

    return year_month_list


def get_time_list(
    stats_type: str | list[str],
    data_kind: str | list[str],
    start_time: datetime,
    end_time: datetime,
    near_real_time: bool = False,
    **kwargs,
) -> list[datetime]:

    time_list = []

    __start_time = start_time.replace(
        hour=(start_time.hour // 6) * 6, minute=0, second=0, microsecond=0
    )
    __end_time = end_time.replace(
        hour=(end_time.hour // 6) * 6, minute=0, second=0, microsecond=0
    )

    start_year = __start_time.year
    start_month = __start_time.month
    end_year = __end_time.year
    end_month = __end_time.month

    if not near_real_time:
        year_month_list = get_year_month_list(
            start_year, start_month, end_year, end_month
        )
        for year, month in year_month_list:
            time_list.append(datetime(year, month, 1, 0))

    else:
        if stats_type == "instant":
            time = __start_time
            while time <= __end_time:
                time_list.append(time)
                time += timedelta(hours=6)
        if stats_type == "monthly":
            year_month_list = get_year_month_list(
                start_year, start_month, end_year, end_month
            )
            for year, month in year_month_list:
                time_list.append(datetime(year, month, 1, 0))
        if stats_type == "diurnal":
            year_month_list = get_year_month_list(
                start_year, start_month, end_year, end_month
            )
            for year, month in year_month_list:
                for hour in [0, 6, 12, 18]:
                    time_list.append(datetime(year, month, 1, hour))

    return time_list


def jra3Q_download(
    stats_type: str | list[str],
    data_kind: str | list[str],
    var: str | list[str],
    near_real_time: bool | str,
    start_time: datetime,
    end_time: datetime,
    base_dir: Path,
    log_file_fpath: Path,
    exist_skip: bool = False,
    **kwargs,
) -> None:

    download_list = []

    if stats_type == "all":
        stats_type_list = ["instant", "monthly", "diurnal"]
    else:
        stats_type_list = stats_type if isinstance(stats_type, list) else [stats_type]

    if data_kind == "all":
        data_kind_list = code_dict.keys()
    else:
        data_kind_list = data_kind if isinstance(data_kind, list) else [data_kind]

    if near_real_time == "all":
        near_real_time_list = [True, False]
    else:
        near_real_time_list = [True] if near_real_time else [False]

    for data_kind in data_kind_list:
        for stats_type in stats_type_list:

            if (data_kind == "anl_snow125") and (stats_type in ["monthly", "diurnal"]):
                continue

            if var == "all":
                var_list = code_dict[data_kind].keys()
            else:
                var_list = var if isinstance(var, list) else [var]
                var_list = [
                    var for var in var_list if var in code_dict[data_kind].keys()
                ]

            for __var in var_list:
                for __near_real_time in near_real_time_list:
                    time_list = get_time_list(
                        stats_type, data_kind, start_time, end_time, __near_real_time
                    )

                    for time in time_list:

                        if stats_type in ["monthly", "diurnal"]:
                            sd_list = [False, True]
                        else:
                            sd_list = [False]

                        for __sd in sd_list:

                            url = get_url(
                                stats_type,
                                data_kind,
                                __var,
                                time.year,
                                time.month,
                                time.day,
                                time.hour,
                                __sd,
                                __near_real_time,
                            )
                            save_fpath = get_save_fpath(
                                base_dir,
                                stats_type,
                                data_kind,
                                __var,
                                time.year,
                                time.month,
                                time.day,
                                time.hour,
                                __sd,
                                __near_real_time,
                            )

                            download(
                                url,
                                save_fpath,
                                log_file_fpath=log_file_fpath,
                                download_method="util_url_noauth",
                                exist_skip=exist_skip,
                            )
