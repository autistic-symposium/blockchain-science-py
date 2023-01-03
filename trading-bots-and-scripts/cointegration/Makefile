.PHONY: clean install install_deps deploy_bot

clean:
	@find . -iname '*.py[co]' -delete
	@find . -iname '__pycache__' -delete
	@rm -rf  '.pytest_cache'
	@rm -rf dist/
	@rm -rf build/
	@rm -rf *.egg-info
	@rm -rf .tox
	@rm -rf venv/lib/python*/site-packages/*.egg
	@rm -rf results/*csv results/*png

install:
	python3 setup.py install

install_deps:
	pip3 install -r requirements.txt

deploy_bot:
	cointbot -b