.PHONY: setup.py requirements.txt

DIST_BASENAME := $(shell poetry version | tr '-' '_' | tr ' ' '-')

build: setup.py requirements.txt

setup.py:
	poetry build && \
	tar --strip-components=1 -xvf dist/$(DIST_BASENAME).tar.gz '*/setup.py'

requirements.txt:
	poetry export --without-hashes > requirements.txt
