from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from ...util import Dataset
from . import dl


class COBESST(Dataset):
    def __init__(self) -> None:
        super().__init__()

        self.min_time = datetime(1850, 1, 1)

    def get_request_key(
        self, download_kw: dict[str, list[str]], **kwargs
    ) -> list[dict[str, Any]]:

        return [{"": None}]

    def get_request_time_range(
        self, start_time: datetime, end_time: datetime, request_kw: dict[str, Any]
    ) -> tuple[datetime, datetime]:

        min_start_time = self.min_time
        max_end_time = datetime.now() - timedelta(days=16)

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

        return {"": [""]}

    def dl_file(
        self,
        start_time: datetime,
        end_time: datetime,
        request_kw: dict[str, Any],
        data_dir: Path,
        exist_ok: bool = False,
    ) -> None:

        dl.cobesst_download(
            start_time,
            end_time,
            data_dir,
            exist_ok,
        )

    def get_newest_time(self, request_kw: dict[str, list[Any]]) -> datetime:
        return datetime.now() - timedelta(days=90)
