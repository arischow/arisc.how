from pathlib import Path

PROJECT_ROOT_DIR = Path(__file__).parent.parent.resolve()
SRC_DIR = Path.joinpath(PROJECT_ROOT_DIR, "src")
TEMPLATE_DIR = Path.joinpath(SRC_DIR, "templates")
DIST_DIR = Path.joinpath(PROJECT_ROOT_DIR, "dist")
