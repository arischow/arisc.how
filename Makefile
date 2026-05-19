build: build/js build/py

build/py:
	poetry run build

build/js: node_modules
	npx tailwindcss -o "./dist/static/output.css"

node_modules: package.json
	npm install
	@touch node_modules

dev: node_modules build
	trap 'kill 0' EXIT; \
	npx wrangler pages dev "$(CURDIR)/dist" & \
	watchman-make -p 'frontend/**' 'contents/**' 'src/**' 'Makefile*' -t build

watch:
	watchman-make -p 'frontend/**' 'contents/**' 'src/**' 'Makefile*' -t build
