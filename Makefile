SHELL := cmd.exe
.SHELLFLAGS := /c

VENV = venv
PYTHON = $(VENV)/Scripts/python.exe
PIP = $(VENV)/Scripts/pip.exe
PY_REQ = requirements.txt

INPUT_FILE ?= test_input.txt
OUTPUT_DIR ?= test_output
OUTPUT_FILE ?= $(OUTPUT_DIR)/$(INPUT_FILE)
FILE_SIZE ?= 524288000

.PHONY: install check clean pep runS runC test

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
	@if exist $(OUTPUT_DIR) rmdir /s /q $(OUTPUT_DIR)
	@if exist $(INPUT_FILE) del /q $(INPUT_FILE)

pep:
	@$(PYTHON) -m pycodestyle *.py

runS:
	@$(PYTHON) server.py $(ARGS)

runC:
	@$(PYTHON) client.py $(ARGS)

test: clean install
	@powershell -Command "$$r = New-Object Random; $$chars = 'abcdefghijklmnopqrstuvwxyz0123456789'; $$block = -join (1..1024 | ForEach-Object { $$chars[$$r.Next($$chars.Length)] }); $$sw = [IO.StreamWriter]::new('$(INPUT_FILE)'); for ($$i = 0; $$i -lt [math]::Ceiling($(FILE_SIZE)/1024); $$i++) { $$sw.Write($$block) }; $$sw.Close()"
	@powershell -Command "Start-Process -FilePath '$(PYTHON)' -ArgumentList 'server.py --output $(OUTPUT_DIR)'"
	@timeout /t 2 /nobreak >nul
	@$(PYTHON) client.py --input $(INPUT_FILE)
	@certutil -hashfile $(INPUT_FILE) SHA256
	@certutil -hashfile $(OUTPUT_FILE) SHA256
