.PHONY: clean install lint

install:
	poetry install

clean:
	@find . -iname '__pycache__' -delete
	poetry cache clear
	poetry env remove --all

lint:
	tox -e lint