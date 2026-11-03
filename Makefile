.PHONY: build test check doctor preview
build:
	python3 scripts/build.py
test:
	python3 -m unittest discover -s tests -v
check: build test
	python3 scripts/check.py
	node --check site/site.js
doctor:
	python3 scripts/capability.py doctor
preview: build
	python3 -m http.server 8000 --bind 127.0.0.1 --directory _site
