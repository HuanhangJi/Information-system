
import os.path
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
print()
BASE_DIR = os.path.join(BASE_DIR,'front')
print(BASE_DIR)