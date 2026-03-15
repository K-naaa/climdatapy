#! /usr/bin/env python3


from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from ...util import Dataset
from .param import code_dict
from . import dl


class JRA3Q(Dataset):

    def get_request_key(
        self, download_kw: dict[str, list[Any]], **kwargs
    ) -> list[dict[str, Any]]:

        request_key_list = []

        # download_kwのallを展開
        if "all" in download_kw["stats_type"]:
            download_kw["stats_type"] = ["instant", "monthly", "diurnal"]
        if "all" in download_kw["data_kind"]:
            download_kw["data_kind"] = [
                "anl_surf125",
                "anl_p125",
                "anl_isentrop125",
                "anl_land125",
                "anl_snow125",
            ]
        if "all" in download_kw["near_realtime"]:
            download_kw["near_realtime"] = [False, True]

        for stats_type in download_kw["stats_type"]:
            # 瞬間値 or 統計値
            for data_kind in download_kw["data_kind"]:
                # 解析値 or 予報値, 解像度
                # 瞬間値以外の積雪データは飛ばす
                if (data_kind == "anl_snow125") and (stats_type != "instant"):
                    continue
                for near_realtime in download_kw["near_realtime"]:
                    # 全期間 or 準リアルタイム
                    if near_realtime:
                        # 準リアルタイム
                        request_key_list.append(
                            {
                                "stats_type": stats_type,
                                "data_kind": data_kind,
                                "near_realtime": near_realtime,
                                "std": False,
                            }
                        )
                        if download_kw["std"]:
                            request_key_list.append(
                                {
                                    "stats_type": stats_type,
                                    "data_kind": data_kind,
                                    "near_realtime": near_realtime,
                                    "std": True,
                                }
                            )
                    else:
                        # 全期間
                        if "all" in download_kw["var"]:
                            download_kw["var"] = list(code_dict[data_kind].keys())
                        for var in download_kw["var"]:
                            request_key_list.append(
                                {
                                    "stats_type": stats_type,
                                    "data_kind": data_kind,
                                    "near_realtime": near_realtime,
                                    "var": var,
                                    "std": False,
                                }
                            )
                            if download_kw["std"]:
                                request_key_list.append(
                                    {
                                        "stats_type": stats_type,
                                        "data_kind": data_kind,
                                        "near_realtime": near_realtime,
                                        "var": var,
                                        "std": True,
                                    }
                                )

        return request_key_list

    def dl_file(
        self,
        start_time: datetime,
        end_time: datetime,
        request_kw: dict[str, Any],
        data_dir: Path,
        exist_ok: bool = False,
    ) -> None:
        dl.jra3Q_download(
            request_kw["stats_type"],
            request_kw["data_kind"],
            request_kw["var"],
            request_kw["near_realtime"],
            start_time,
            end_time,
            data_dir,
            exist_ok,
        )

    def get_newest_time(self, request_kw: dict[str, list[Any]]) -> datetime:

        if request_kw["near_realtime"]:
            last_time = datetime.now() - timedelta(days=4)
            last_time = datetime(last_time.year, last_time.month, last_time.day, 18)
        else:
            last_time = datetime.now() - timedelta(days=4)

        return last_time
