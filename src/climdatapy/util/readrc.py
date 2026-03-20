#! /usr/bin/env python3

from pathlib import Path
from typing import Dict


def load_climdatarc(dir: Path = Path.home()) -> Dict[str, str]:

    path = dir / ".climdatarc"

    data: Dict[str, str] = {}

    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                k, v = line.split("=", 1)
                data[k.strip()] = v.strip()

    return data
