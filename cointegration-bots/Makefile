.PHONY: 
clean:
	@find . -iname '*.py[co]' -delete
	@find . -iname '__pycache__' -delete
	@rm -rf  '.pytest_cache'
	@rm -rf dist/
	@rm -rf build/
	@rm -rf *.egg-info
	@rm -rf .tox
	@rm -rf venv/lib/python*/site-packages/*.egg

.PHONY: clean_data
clean_data:
	@rm -rf results/*csv results/*json results/*png

.PHONY: install
install:
	python3 setup.py install

.PHONY: install_deps
install_deps:
	pip3 install -r requirements.txt

.PHONY: dc_prune
dc_prune:
	docker system prune

.PHONY: bot1
bot1:
	@echo "Deploying bot 1 on a docker container"
	@bash ./docker/bot1/run_bot1.sh

.PHONY: build_bot1
build_bot1:
	docker-compose -f ./docker/bot1/docker-compose.yml build --no-cache

.PHONY: up_bot1
up_bot1:
	docker-compose -f ./docker/bot1/docker-compose.yml up

.PHONY: down_bot1
down_bot1:
	docker-compose -f ./docker/docker-compose-bot1.yml down

.PHONY: logs_bot1
logs_bot1:
	docker-compose -f ./docker/docker-compose-bot1.yml logs -f


