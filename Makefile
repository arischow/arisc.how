build:
	poetry run build

watch:
	watchman-make -p 'frontend/**/*.html' 'contents/**' 'Makefile*' -t build
