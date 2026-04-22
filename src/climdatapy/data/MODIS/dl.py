#! /usr/bin/env python3

from datetime import datetime, timedelta
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from ...util import load_climdatarc

def modis_download(
    product,
    start_time,
    end_time,
    base_dir,
    exist_skip=False,
):
    #認証情報を取得
    d = load_climdatarc()
    username = d["ModisUsername"]
    passward = d["ModisPassward"]

    #セッション作成
    session = requests.Session()
    session.auth=(username,passward)


    current = start_time

    while current <= end_time:

        year = current.year
        doy = current.timetuple().tm_yday

        # ディレクトリURL
        dir_url = (
            f"https://ladsweb.modaps.eosdis.nasa.gov/archive/allData/62/"
            f"{product}/{year}/{doy:03}/"
        )

        # 一覧取得
        res = requests.get(dir_url)
        if res.status_code != 200:
            print(f"Failed to access {dir_url}")
            current += timedelta(days=1)
            continue

        soup = BeautifulSoup(res.text, "html.parser")

        filenames = [
            a.get("href")
            for a in soup.find_all("a")
            if a.get("href") and a.get("href").endswith(".nc")
        ]

        if not filenames:
            print(f"No nc file for {year}-{doy}")
            current += timedelta(days=1)
            continue

        filename = Path(filenames[0]).name

        url = dir_url + filename

        save_path = Path(base_dir) / str(year) / f"{doy:03}" / filename
        save_path.parent.mkdir(parents=True, exist_ok=True)

        if not (exist_skip and save_path.exists()):
            print(f"Downloading: {filename}")
            r = session.get(url, stream=True)
            r.raise_for_status()
            with open(save_path, "wb") as f:
                f.write(r.content)

        current += timedelta(days=1)