import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.resolve()))
from get_file_paths import rgetFilePaths

print(rgetFilePaths('.', '*.md'))