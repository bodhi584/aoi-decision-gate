"""Download the Siemens AOI data set (Pfab et al. 2024, Mendeley Data, DOI 10.17632/99jzmh9658.2).

The data are licensed CC BY-NC 3.0 and owned by Siemens AG, so they are not stored in this repository.
Usage: python scripts/download_data.py   ->  data/dataset.csv, data/mapping.json
"""
import hashlib
import sys
import urllib.request
from pathlib import Path

BASE = "https://data.mendeley.com/public-files/datasets/99jzmh9658/files/{}/file_downloaded"
FILES = {
    "dataset.csv": ("3bcbede5-358b-489a-b4b8-9ac3a06e89b9", "53e8568743216d556856ed69b388f6750fbfa0b8c59ad31f970515ac9eb10e62"),
    "mapping.json": ("e22624d7-0124-410c-8528-715b1e1c8c87", "3b20f440b6d9ed0baefa662e1a6f03688befbe0f28341a3b54655d3058c6e486"),
}


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main(out: str = "data") -> None:
    out_dir = Path(out)
    out_dir.mkdir(exist_ok=True)
    for name, (fid, digest) in FILES.items():
        p = out_dir / name
        if not p.exists() or sha256(p) != digest:
            print(f"downloading {name} ...", flush=True)
            urllib.request.urlretrieve(BASE.format(fid), p)
        if sha256(p) != digest:
            sys.exit(f"checksum mismatch for {name}")
        print(f"{name}: ok")


if __name__ == "__main__":
    main(*sys.argv[1:])
