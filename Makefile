build: build/js build/py

build/py:
	poetry run build

build/js:
	npx tailwindcss -o "./dist/static/output.css"

dev: build
	trap 'kill 0' EXIT; \
	npx wrangler pages dev ./dist & \
	watchman-make -p 'frontend/**' 'contents/**' 'src/**' 'Makefile*' -t build

watch:
	watchman-make -p 'frontend/**' 'contents/**' 'src/**' 'Makefile*' -t build
