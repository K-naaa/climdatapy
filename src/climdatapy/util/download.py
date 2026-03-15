#! /usr/bin/env python3

from pathlib import Path
import requests
from requests.exceptions import HTTPError, ChunkedEncodingError
import time
import warnings


MAX_TRIAL = 3


def download_noauth(
    url: str,
    save_fpath: Path,
    chunk_size: int = 8192,
    sleep_time: float = 1.0,
    exist_skip: bool = False,
    **kwargs,
) -> None:
    """
    Download files from a URL without authentication.

    Parameters
    ----------
    url : str
        URL to download from.
    save_fpath : Path
        File path where the file will be saved.
    chunk_size : int, optional
        Download chunk size, by default 8192
    sleep_time : float, optional
        waiting time before downloading a next file., by default 1.0
    exist_skip : bool, optional
        if True, Skip files if they already exist., by default False
    """

    save_fpath.parent.mkdir(parents=True, exist_ok=True)

    for i in range(MAX_TRIAL):
        try:
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                with open(save_fpath, "wb") as f:
                    for chunk in r.iter_content(chunk_size=chunk_size):
                        if chunk:
                            f.write(chunk)
            break
        except HTTPError:
            warnings.warn(f'HTTP Error while downloading "{url}".', stacklevel=4)
        except ChunkedEncodingError as e:
            if i == 2:
                raise
    time.sleep(sleep_time)


def download(
    url: str,
    save_fpath: Path,
    download_method: str,
    exist_skip: bool = False,
    **kwargs,
) -> None:

    # file existence check
    if exist_skip and save_fpath.exists():
        return
    else:
        if download_method == "util_url_noauth":
            download_noauth(url, save_fpath, exist_skip=exist_skip, **kwargs)
        else:
            raise ValueError(f'download_method "{download_method}" is invalid')
