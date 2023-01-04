.PHONY: clean install install_deps bot1

clean:
	@find . -iname '*.py[co]' -delete
	@find . -iname '__pycache__' -delete
	@rm -rf  '.pytest_cache'
	@rm -rf dist/
	@rm -rf build/
	@rm -rf *.egg-info
	@rm -rf .tox
	@rm -rf venv/lib/python*/site-packages/*.egg
	@rm -rf results/*csv results/*png results/*json

install:
	python3 setup.py install

install_deps:
	pip3 install -r requirements.txt

bot1:
	@echo "Deploying bot 1 on a docker container"
	@bash ./docker/run_bot1.sh
