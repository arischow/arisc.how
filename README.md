# arisc.how

The source code of https://arisc.how

## Development

```
make watch
npx tailwindcss -i ./frontend/tailwind/input.css -o ./dist/static/output.css --watch
browser-sync start --server --files "./dist/**"
```
