#! /usr/bin/env python3

from . import data
from .util import Dataset

DATASET_REGISTRY = {
    "JRA3Q": data.JRA3Q,
    "NCEP1": data.NCEP1,
    "NCEP2": data.NCEP2,
    "OISST": data.OISST,
    "COBESST": data.COBESST,
    "HIMSST": data.HIMSST,
}


def get_manager(name: str) -> Dataset:
    """データセット管理クラスを取得

    Parameters
    ----------
    name : str
        データセット名

    Returns
    -------
    Dataset
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
