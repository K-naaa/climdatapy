#! /usr/bin/env python3

import copernicusmarine
from datetime import datetime, timedelta
from pathlib import Path
import logging
import sys
import contextlib
import os
from typing import Iterator
import time

from ...util import load_climdatarc

DATASET_ID = "METOFFICE-GLO-SST-L4-NRT-OBS-SST-V2"
SLEEP_TIME = 1.0


@contextlib.contextmanager
def suppress_output() -> Iterator[None]:
    old_stdout = sys.stdout
    old_stderr = sys.stderr

    loggers = [logging.getLogger()] + [
        logging.getLogger(name) for name in logging.root.manager.loggerDict
    ]

    saved_handlers = {lg: lg.handlers[:] for lg in loggers}

    try:
        devnull = open(os.devnull, "w")

        sys.stdout = devnull
        sys.stderr = devnull

        for lg in loggers:
            lg.handlers = [
                h
                for h in lg.handlers
                if not (
                    isinstance(h, logging.StreamHandler)
                    and getattr(h, "stream", None) in (old_stdout, old_stderr)
                )
            ]

        yield

    finally:

        sys.stdout = old_stdout
        sys.stderr = old_stderr
        for lg, handlers in saved_handlers.items():
            lg.handlers = handlers
        devnull.close()


def get_save_fpath(time: datetime, data_dir: Path) -> Path:

    return data_dir / Path(
        (
            "OSTIA/SST_GLO_SST_L4_NRT_OBSERVATIONS_010_001"
            f"/METOFFICE-GLO-SST-L4-NRT-OBS-SST-V2/{time:%Y}/{time:%m}"
            f"/{time:%Y%m%d}120000-UKMO-L4_GHRSST-SSTfnd-OSTIA-GLOB-v02.0-fv02.0.nc"
        )
    )


def ostia_download(
    start_time: datetime,
    end_time: datetime,
    data_dir: Path,
    exist_skip: bool,
    **kwargs,
) -> None:

    d = load_climdatarc()
    username = d["CopernicusMarineUsername"]
    passward = d["CopernicusMarinePassward"]

    time_list = [start_time]
    while time_list[-1] < end_time:
        time_list.append(time_list[-1] + timedelta(days=1))

    for t in time_list:

        save_fpath = get_save_fpath(t, data_dir)

        if not (exist_skip and save_fpath.exists()):

            logging.info(f"try to download {save_fpath.name}")

            with suppress_output():
                copernicusmarine.get(
                    username=username,
                    password=passward,
                    dataset_id=DATASET_ID,
                    filter=f"*{t:%Y%m%d}*",
                    output_directory=data_dir / Path("OSTIA"),
                    skip_existing=exist_skip,
                    disable_progress_bar=True,
                )
                time.sleep(SLEEP_TIME)
            logging.info(f" =(file conversion)=> {save_fpath}")

        else:
            logging.info(f"{save_fpath} is already existed.")
