build:
	poetry run build

watch:
	watchman-make -p 'frontend/**' 'contents/**' 'src/**' 'Makefile*' -t build
