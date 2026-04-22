#! /usr/bin/env python3

from datetime import datetime
from pathlib import Path

from ...util import Dataset
from . import dl


class MODIS(Dataset):

    
    def get_request_key(self, download_kw, **kwargs):
        return [{}]

    def get_request_time_range(self, start_time, end_time, request_kw):
        return start_time, end_time

    def get_all_download_key(self):
        return {}

    def get_newest_time(self, request_kw):
        return datetime.now()

    
    def dl_file(
        self,
        start_time: datetime,
        end_time: datetime,
        request_kw: dict,
        data_dir: Path,
        exist_ok: bool = False,
    ) -> None:

        dl.modis_download(
            product="MCD06COSP_D3_MODIS",
            start_time=start_time,
            end_time=end_time,
            base_dir=data_dir,
            exist_skip=exist_ok,
        )