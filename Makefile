build:
	poetry run build

watch:
	watchman-make -p 'frontend/**/*.jinja2' 'contents/**' 'Makefile*' -t build
