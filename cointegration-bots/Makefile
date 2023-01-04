.PHONY: clean clean_data install install_deps bot1 bot2

clean:
	@find . -iname '*.py[co]' -delete
	@find . -iname '__pycache__' -delete
	@rm -rf  '.pytest_cache'
	@rm -rf dist/
	@rm -rf build/
	@rm -rf *.egg-info
	@rm -rf .tox
	@rm -rf venv/lib/python*/site-packages/*.egg

clean_data:
	@rm -rf results/*csv results/*png results/*json

install:
	python3 setup.py install

install_deps:
	pip3 install -r requirements.txt

bot1:
	@echo "Deploying bot 1 on a docker container"
	@bash ./docker/run_bot1.sh

bot2:
	@echo "Deploying bot 2 on a docker container"
	@bash ./docker/run_bot2.sh
