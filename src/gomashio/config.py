from pathlib import Path

PROJECT_ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
FRONTEND_DIR = Path.joinpath(PROJECT_ROOT_DIR, "frontend")
TEMPLATE_DIR = Path.joinpath(FRONTEND_DIR, "templates")
CONTENTS_DIR = Path.joinpath(PROJECT_ROOT_DIR, "contents")
DIST_DIR = Path.joinpath(PROJECT_ROOT_DIR, "dist")
