#! /usr/bin/env python3

from . import data

DATASET_REGISTRY = {"JRA3Q": data.JRA3Q}


def get_manager(name: str):

    try:
        return DATASET_REGISTRY[name]()
    except KeyboardInterrupt:
        raise ValueError(f"Unknown dataset: {name}")
