#! /usr/bin/env python3

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any
from tqdm import tqdm

from .log import log_to_file


class Dataset(ABC):
    """
    気象・海洋データセットを管理する抽象基底クラス
    """

    @abstractmethod
    def get_request_key(
        self,
        download_kw: dict[str, list[str]],
        **kwargs,
    ) -> list[dict[str, Any]]:
        """与えられたdownload_keyの組み合わせ(直積)を返す

        Parameters
        ----------
        download_kw : dict[str, list[str]]
            データセット固有のダウンロードkeyword

        Returns
        -------
        list[dict[str, Any]]
            download_kwの各keyについての直積
        """

        pass

    @abstractmethod
    def get_request_time_range(
        self, start_time: datetime, end_time: datetime, request_kw: dict[str, Any]
    ) -> tuple[datetime, datetime]:
        """ダウンロード可能な時刻範囲を取得。
        データセットの公開期間のみ抽出する。

        Parameters
        ----------
        start_time : datetime
            ダウンロード開始時刻
        end_time : datetime
            ダウンロード終了時刻
        request_kw : dict[str, Any]
            ファイルの設定

        Returns
        -------
        tuple[datetime, datetime]
            ダウンロード可能な最小・最大時刻。
            start_time, end_timeがデータセットの公開期間内の場合、(start_time, end_time)
        """

        pass

    @abstractmethod
    def get_all_download_key(self) -> dict[str, list[str]]:
        """指定可能な最大限のdownload_keyを取得

        Returns
        -------
        dict[str, list[str]]
            指定可能な最大限のdownload_key
        """

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
        """指定した時間範囲・request_kwを満たすファイルをダウンロード

        Parameters
        ----------
        start_time : datetime
            ダウンロード開始時刻
        end_time : datetime
            ダウンロード終了時刻
        request_kw : dict[str, Any]
            データセット固有のファイル情報
        data_dir : Path
            データセットを保存するディレクトリ
        exist_ok : bool, optional
            Trueならば、既にファイルが存在する場合はスキップ, by default False
        """

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
        **kwargs,
    ) -> None:
        """データセットをダウンロード

        Parameters
        ----------
        start_time : datetime
            ダウンロード開始時刻
        end_time : datetime
            ダウンロード終了時刻
        download_kw : dict[str, list[str]]
            データセット固有のファイル情報
        data_dir : Path
            データセットを保存するディレクトリのファイルパス
        log_file_path : Path
            ログを出力するファイルパス
        exist_ok : bool, optional
            Trueならば、既にファイルが存在する場合はスキップ, by default False
        """

        request_kw_list = self.get_request_key(download_kw)

        for request_kw in tqdm(request_kw_list, desc=f"{self.__class__.__name__}"):
            request_start_time, request_end_time = self.get_request_time_range(
                start_time, end_time, request_kw
            )
            self.dl_file(
                request_start_time, request_end_time, request_kw, data_dir, exist_ok
            )

    def download_all(
        self,
        start_time: datetime,
        end_time: datetime,
        data_dir: Path,
        log_file_path: Path,
        exist_ok: bool = False,
    ) -> None:
        """指定した時間範囲に含まれる指定可能なすべての関数をダウンロード。
        downloadメソッドのwrapper。

        Parameters
        ----------
        start_time : datetime
            ダウンロード開始時刻
        end_time : datetime
            ダウンロード終了時刻
        data_dir : Path
            データセットを保存するディレクトリのファイルパス
        log_file_path : Path
            ログファイルのファイルパス
        exist_ok : bool, optional
            Trueならば、既にファイルが存在する場合はスキップ, by default False
        """

        self.download_key = self.get_all_download_key()
        self.download(
            start_time, end_time, self.download_key, data_dir, log_file_path, exist_ok
        )

    @abstractmethod
    def get_newest_time(self, request_kw: dict[str, list[Any]]) -> datetime:
        """ダウンロード可能な最新ファイルの時刻を取得

        Parameters
        ----------
        request_kw : dict[str, list[Any]]
            データセット固有の情報

        Returns
        -------
        datetime
            最新ファイルの時刻
        """

        pass

    @log_to_file()
    def update(
        self,
        download_kw: dict[str, list[str]],
        data_dir: Path,
        log_file_path: Path,
        exist_ok: bool = False,
    ) -> None:
        """最新のファイルをダウンロード。

        Parameters
        ----------
        download_kw : dict[str, list[str]]
            データセット固有の情報
        data_dir : Path
            データセットを保存するディレクトリ
        log_file_path : Path
            ログファイルのファイルパス
        exist_ok : bool, optional
            Trueならば、既にファイルが存在する場合はスキップ, by default False
        """

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
        """取得可能なすべてのファイルの種類について、最新時刻のデータをダウンロード。
        updateメソッドのwrapper。

        Parameters
        ----------
        data_dir : Path
            データセットを保存するファイルパス
        log_file_path : Path
            ログファイルのファイルパス
        exist_ok : bool, optional
            Trueならば、既にファイルが存在する場合はスキップ, by default False
        """

        download_key = self.get_all_download_key()
        self.update(download_key, data_dir, log_file_path, exist_ok)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"
