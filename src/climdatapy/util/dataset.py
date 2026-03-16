#! /usr/bin/env python3

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any
from tqdm import tqdm

from .log import log_to_file


class Dataset(ABC):
    """
    気象・海洋データセットを管理する抽象クラス
    """

    @abstractmethod
    def get_request_key(
        self,
        download_kw: dict[str, list[str]],
        **kwargs,
    ) -> list[dict[str, Any]]:

        pass

    @abstractmethod
    def get_all_download_key(self) -> dict[str, list[str]]:

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

    @log_to_file()
    def download(
        self,
        start_time: datetime,
        end_time: datetime,
        download_kw: dict[str, list[str]],
        data_dir: Path,
        log_file_path: Path,
        exist_ok: bool = False,
    ) -> None:

        request_kw_list = self.get_request_key(download_kw)

        for request_kw in tqdm(request_kw_list, desc=f"{self.__class__.__name__}"):
            self.dl_file(start_time, end_time, request_kw, data_dir, exist_ok)

    def download_all(
        self,
        start_time: datetime,
        end_time: datetime,
        data_dir: Path,
        log_file_path: Path,
        exist_ok: bool = False,
    ) -> None:

        self.download_key = self.get_all_download_key()
        self.download(
            start_time, end_time, self.download_key, data_dir, log_file_path, exist_ok
        )

    @abstractmethod
    def get_newest_time(self, request_kw: dict[str, list[Any]]) -> datetime:

        pass

    @log_to_file()
    def update(
        self,
        download_kw: dict[str, list[str]],
        data_dir: Path,
        log_file_path: Path,
        exist_ok: bool = False,
    ) -> None:

        request_kw_list = self.get_request_key(download_kw)
        for request_kw in request_kw_list:
            end_time = self.get_newest_time(request_kw)
            start_time = end_time - timedelta(days=10)
            self.dl_file(start_time, end_time, request_kw, data_dir, exist_ok)

    def update_all(
        self,
        data_dir: Path,
        log_file_path: Path,
        exist_ok: bool = False,
    ) -> None:

        download_key = self.get_all_download_key()
        self.update(download_key, data_dir, log_file_path, exist_ok)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"
