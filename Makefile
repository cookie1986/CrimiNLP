.ONESHELL:

.DEFAULT_GOAL := run

PYTHON = ./venv/bin/python3
PIP = ./venv/bin/pip

venv/bin/activate: requirements.txt
	python3 -m venv venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

venv: venv/bin/activate
	. ./venv/bin/activate

RUN_ARGS = 

run: venv
	$(PYTHON) main.py ${RUN_ARGS}

clean: 
	rm -rf __pycache__
	rm -rf venv