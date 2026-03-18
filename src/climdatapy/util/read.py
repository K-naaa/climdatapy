#! /usr/bin/env python3

import requests
from requests.exceptions import (
    HTTPError,
    ChunkedEncodingError,
    ConnectionError,
    ReadTimeout,
)
import time
import warnings

MAX_TRIAL = 3


def read_as_str(url, sleep_time: float = 1.0) -> str | None:

    for i in range(MAX_TRIAL):
        try:
            response: requests.Response = requests.get(url, timeout=60)
            time.sleep(sleep_time)
            response.raise_for_status()

            return response.text

        except HTTPError:
            warnings.warn(f'HTTP Error while downloading "{url}".', stacklevel=4)
        except ConnectionError:
            warnings.warn(f'ConnectionError while downloading "{url}".', stacklevel=4)
        except ReadTimeout:
            warnings.warn(f'Read Timeout while downloading "{url}".', stacklevel=4)
        except ChunkedEncodingError:
            warnings.warn(
                f'ChunkedEncodingError while downloading "{url}".', stacklevel=4
            )
