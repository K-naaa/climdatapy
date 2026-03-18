#! /usr/bin/env python3

from datetime import datetime, timedelta
from typing import Any

from ...util import Dataset
from . import dl


class NCEP1(Dataset):

    def __init__(self) -> None:

        super().__init__()

        self.ncep12_short_name = "Reanalysis1"
        self.prs_vars = dl.prs_vars_re1
        self.srf_vars = dl.srf_vars_re1
        self.ncep12_min_time = datetime(1948, 1, 1)

    def get_request_key(
        self, download_kw: dict[str, list[str]], **kwargs
    ) -> list[dict[str, Any]]:

        if "all" in download_kw["stats_type"]:
            download_kw["stats_type"] = ["6hourly", "daily", "monthly"]
        if "all" in download_kw["data_kind"]:
            download_kw["data_kind"] = ["pressure", "surface"]
        if "all" in download_kw["var"]:
            download_kw["var"] = self.prs_vars + self.srf_vars

        request_key_list = []

        for stats_type in download_kw["stats_type"]:
            for data_kind in download_kw["data_kind"]:

                all_vars = self.prs_vars if data_kind == "pressure" else self.srf_vars
                for var in download_kw["var"]:
                    if var in all_vars:
                        request_key_list.append(
                            {
                                "stats_type": stats_type,
                                "data_kind": data_kind,
                                "var": var,
                            }
                        )

        return request_key_list

    def get_request_time_range(
        self, start_time: dl.datetime, end_time: dl.datetime, request_kw: dict[str, Any]
    ) -> tuple[datetime, datetime]:

        min_start_time = self.ncep12_min_time
        max_end_time = datetime.now() - timedelta(days=5)

        request_start_time = (
            start_time if min_start_time < start_time else min_start_time
        )

        if end_time < request_start_time:
            request_end_time = request_start_time
        elif end_time > max_end_time:
            request_end_time = max_end_time

        else:
            request_end_time = end_time

        return request_start_time, request_end_time

    def get_all_download_key(self) -> dict[str, list[str]]:

        return {
            "data_kind": ["all"],
            "stats_type": ["all"],
            "var": ["all"],
        }

    def dl_file(
        self,
        start_time: datetime,
        end_time: datetime,
        request_kw: dict[str, Any],
        data_dir: dl.Path,
        exist_ok: bool = False,
    ) -> None:

        dl.ncep12_download(
            start_time,
            end_time,
            self.ncep12_short_name,
            request_kw["stats_type"],
            request_kw["data_kind"],
            request_kw["var"],
            data_dir,
            exist_ok,
        )

    def get_newest_time(self, request_kw: dict[str, list[Any]]) -> datetime:

        return datetime.now() - timedelta(days=5)


class NCEP2(NCEP1):

    def __init__(self) -> None:

        super().__init__()
        self.ncep12_short_name = "Reanalysis2"
        self.prs_vars = dl.prs_vars_re2
        self.srf_vars = dl.srf_vars_re2
        self.ncep12_min_time = datetime(1979, 1, 1)
