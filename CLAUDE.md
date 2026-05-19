# gomashio

Custom static site generator for https://arisc.how. Python + Jinja2 + Tailwind CSS, deployed to Cloudflare Pages.

## Development

```sh
poetry install && npm install   # first time / fresh worktree setup
make dev                        # build + serve at localhost:8788 + auto-rebuild on file changes
```

## Build

`make build` runs Tailwind first (`dist/static/output.css`), then Python (`poetry run build` renders markdown to `dist/`). Order matters -- the `bust_cache` Jinja2 filter hashes the CSS output.

## Worktree notes

All paths in the Makefile, Python config, wrangler.toml, and tailwind.config.js are relative. `make dev` works from any worktree root -- never hardcode absolute paths.

A fresh worktree needs setup before the first build:
1. `npm install` -- node_modules/ is gitignored
2. `poetry install` -- Poetry creates a separate venv per directory

## Code style

Python: black, isort (black profile), flake8. Templates/CSS: 2-space indent. Pre-commit hooks enforce this.
