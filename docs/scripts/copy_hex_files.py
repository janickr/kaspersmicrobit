from pathlib import Path
from shutil import copytree

copytree(Path("hex"), Path("docs", "hex"), dirs_exist_ok=True)