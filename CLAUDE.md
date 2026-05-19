# gomashio

Custom static site generator for https://arisc.how. Python + Jinja2 + Tailwind CSS, deployed to Cloudflare Pages.

## Development

```sh
poetry install   # first time / fresh worktree setup (npm install is automatic via make)
make dev         # build + serve at localhost:8788 + auto-rebuild on file changes
```

## Build

`make build` runs Tailwind first (`dist/static/output.css`), then Python (`poetry run build` renders markdown to `dist/`). Order matters -- the `bust_cache` Jinja2 filter hashes the CSS output.

## Worktree notes

All paths in the Makefile, Python config, wrangler.toml, and tailwind.config.js are relative. `make dev` works from any worktree root -- never hardcode absolute paths.

A fresh worktree needs `poetry install` before the first build (Poetry creates a separate venv per directory). `make dev` and `make build` auto-run `npm install` when `node_modules/` is missing or `package.json` has changed.

## Code style

Python: black, isort (black profile), flake8. Templates/CSS: 2-space indent. Pre-commit hooks enforce this.
