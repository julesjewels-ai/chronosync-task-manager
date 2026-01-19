.PHONY: install run test clean

venv:
	python3 -m venv venv

install: venv
	./venv/bin/pip install -r requirements.txt

run:
	./venv/bin/python main.py --energy 8

test:
	./venv/bin/pytest

clean:
	rm -rf venv
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete