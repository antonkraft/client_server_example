VENV = venv
PYTHON = $(VENV)/Scripts/python.exe
PIP = $(VENV)/Scripts/pip.exe
PY_REQ = requirements.txt

.PHONY: install check clean pep runS runC

install: $(VENV)/pyvenv.cfg

$(VENV)/pyvenv.cfg: $(PY_REQ)
	python3 -m venv $(VENV)
	$(PYTHON) -m pip install --upgrade pip
	$(PIP) install -r $(PY_REQ)

check:
	$(PYTHON) --version

clean:
	@if exist __pycache__ rmdir /s /q __pycache__
	@if exist venv rmdir /s /q venv

pep:
	@$(PYTHON) -m pycodestyle *.py

runS:
	@$(PYTHON) server.py $(ARGS)

runC:
	@$(PYTHON) client.py $(ARGS)
