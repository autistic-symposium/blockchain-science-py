.PHONY: clean install install_deps lint

clean:
	@find . -iname '*.py[co]' -delete
	@find . -iname '__pycache__' -delete
	@rm -rf  '.pytest_cache'
	@rm -rf dist/
	@rm -rf build/
	@rm -rf *.egg-info
	@rm -rf .tox
	@rm -rf venv/lib/python*/site-packages/*.egg

install:
	python3 setup.py install

install_deps:
	pip3 install -r requirements.txt

lint:
	tox -e lint