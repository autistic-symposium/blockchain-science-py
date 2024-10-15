.PHONY: clean
clean:
	@find . -iname '*.py[co]' -delete
	@find . -iname '__pycache__' -delete
	@rm -rf  '.pytest_cache'
	@rm -rf dist/
	@rm -rf build/
	@rm -rf *.egg-info
	@rm -rf .tox
	@rm -rf venv/lib/python*/site-packages/*.egg

.PHONY: install
install:
	python3 setup.py install

.PHONY: install_deps
install_deps:
	pip3 install -r requirements.txt

.PHONY: lint
lint:
	tox -e lint
