import subprocess

from ._info import DATA_DIR

SOURCE = "wget -r -N -c -np https://physionet.org/files/ptbdb/1.0.0/"
DATASET = DATA_DIR / "physionet.org" / "files" / "ptbdb" / "1.0.0"


def dataset_exists() -> bool:
    return DATASET.is_dir()


def download_dataset() -> bool:
    DATA_DIR.mkdir(exist_ok=True)
    subprocess.run(SOURCE, shell=True, check=True, cwd=DATA_DIR.as_posix())
    return dataset_exists()
