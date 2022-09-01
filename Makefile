build: build/py build/js

build/py:
	poetry run build

build/js:
	npx tailwindcss -o build.css --minify

watch:
	watchman-make -p 'frontend/**' 'contents/**' 'src/**' 'Makefile*' -t build
