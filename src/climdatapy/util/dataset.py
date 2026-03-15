#! /usr/bin/env python3

from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any


class Dataset(ABC):
    """
    気象・海洋データセットを管理する抽象クラス
    """

    def __init__(self, name: str, update_now: bool, **kwargs):
        self.name = name
        self.update_now = update_now

    @abstractmethod
    def get_request_key(
        self,
        download_kw: dict[str, list[Any]],
        **kwargs,
    ) -> list[dict[str, Any]]:

        pass

    @abstractmethod
    def dl_file(
        self,
        start_time: datetime,
        end_time: datetime,
        request_kw: dict[str, Any],
        data_dir: Path,
        exist_ok: bool = False,
    ) -> None:

        pass

    def download(
        self,
        start_time: datetime,
        end_time: datetime,
        download_kw: dict[str, list[Any]],
        data_dir: Path,
        exist_ok: bool = False,
    ) -> None:

        request_kw_list = self.get_request_key(download_kw)

        for request_kw in request_kw_list:
            self.dl_file(start_time, end_time, request_kw, data_dir, exist_ok)

    @abstractmethod
    def get_newest_time(self, request_kw: dict[str, list[Any]]) -> datetime:

        pass

    def update(
        self, download_kw: dict[str, Any], data_dir: Path, exist_ok: bool = False
    ) -> None:

        if self.update_now:

            request_kw_list = self.get_request_key(download_kw)
            for request_kw in request_kw_list:
                start_time = self.get_newest_time(request_kw)
                end_time = start_time
                self.dl_file(start_time, end_time, request_kw, data_dir, exist_ok)

        else:
            raise NotImplementedError("update is not supported for this dataset.")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name})"
