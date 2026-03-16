#! /usr/bin/env python3

import argparse

from climdatapy.manager import get_manager, DATASET_REGISTRY


import argparse
from datetime import datetime
from pathlib import Path


def parse_datetime(s: str) -> datetime:

    try:
        return datetime.fromisoformat(s)
    except ValueError:
        return datetime.strptime(s, "%Y%m%d")


def cmd_download(args):

    manager = get_manager(args.dataset)

    manager.download_all(
        start_time=args.start_time,
        end_time=args.end_time,
        data_dir=args.out,
        log_file_path=args.logfile,
    )


def cmd_update(args):
    manager = get_manager(args.dataset)
    manager.update_all(data_dir=args.out, log_file_path=args.logfile)


def cmd_list(args):

    for name in DATASET_REGISTRY:
        print(name)


def main():

    parser = argparse.ArgumentParser(prog="climdata")
    formatter_class = argparse.ArgumentDefaultsHelpFormatter

    subparsers = parser.add_subparsers(dest="command", required=True)

    # download command
    p_download = subparsers.add_parser(
        "download",
        help="download dataset files",
        description="Download files for a specified dataset and time range.",
    )

    p_download.add_argument("dataset", help="dataset name")

    p_download.add_argument(
        "--start_time",
        type=parse_datetime,
        required=True,
        help="start date (YYYY-MM-DD)",
    )

    p_download.add_argument(
        "--end_time",
        type=parse_datetime,
        required=True,
        help="end date (YYYY-MM-DD)",
    )

    p_download.add_argument(
        "--out",
        type=Path,
        default=Path("data"),
        help="output directory",
    )

    p_download.add_argument(
        "--logfile",
        type=Path,
        default=None,
        help="logfile path",
    )

    p_download.set_defaults(func=cmd_download)

    # update command
    p_update = subparsers.add_parser(
        "update",
        help="download latest dataset files",
    )

    p_update.add_argument("dataset", help="dataset name")

    p_update.add_argument(
        "--out",
        type=Path,
        default=Path("data"),
        help="output directory",
    )

    p_update.add_argument(
        "--logfile",
        type=Path,
        default=None,
        help="logfile path",
    )

    p_update.set_defaults(func=cmd_update)

    # list command
    p_list = subparsers.add_parser(
        "list",
        help="List available datasets",
        description="Show all available dataset managers that can be used with climdata.",
    )
    p_list.set_defaults(func=cmd_list)

    args = parser.parse_args()

    args.func(args)
