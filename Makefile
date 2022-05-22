build:
	poetry run build

watch:
	watchman-make -p 'frontend/**/*' 'contents/**' 'Makefile*' -t build
