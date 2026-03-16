#! /usr/bin/env python3

from . import data

DATASET_REGISTRY = {"JRA3Q": data.JRA3Q}


def get_manager(name: str):
    """データセット管理クラスを取得

    Parameters
    ----------
    name : str
        データセット名

    Returns
    -------
    _type_
        データセット管理クラス

    Raises
    ------
    ValueError
        未対応のデータセット
    """

    try:
        return DATASET_REGISTRY[name]()
    except KeyboardInterrupt:
        raise ValueError(f"Unknown dataset: {name}")
