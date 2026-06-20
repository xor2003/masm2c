.PHONY: clean clean-test clean-pyc clean-build docs help lint test check ci-qa ci-pytest ci-asmtests ci-qemu-tests ci-integration bench-parser
.PHONY: bench-parser-postlex bench-parser-cython bench-parser-compare
.DEFAULT_GOAL := help
define BROWSER_PYSCRIPT
import os, webbrowser, sys
try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT
BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts


clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

lint: ## check style with flake8
	flake8



test-all: ## run tests on every Python version with tox
	tox

coverage: ## check code coverage quickly with the default Python
	coverage run --source masm2c -m pytest tests/func

		coverage report -m
		coverage html
		$(BROWSER) htmlcov/index.html

docs: ## generate MkDocs HTML documentation
	mkdocs build
	$(BROWSER) docs/_build/html/index.html

servedocs: ## compile the docs watching for changes
	mkdocs serve
	$(BROWSER) "http://localhost:8000/"

release: clean ## package and upload a release
	python setup.py sdist upload
	python setup.py bdist_wheel upload

dist: clean ## builds source and wheel package
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

install: clean ## install the package to the active Python's site-packages
	python setup.py install
test: $(TESTS)

check: test_insn_tests
	./$<

ci-qa: ## run unified Python quality checks used by CI
	python scripts/qa.py

ci-pytest: ## run project pytest suite
	python -m pytest -q

ci-asmtests: ## run asm translation/regression tests
	python asmTests/run_tests.py $${JOBS:+--jobs $$JOBS}

ci-qemu-tests: ## run qemu-based integration tests
	cd qemu_tests && ./_test.sh

ci-integration: ci-pytest ci-asmtests ci-qemu-tests ## run integration checks used by CI

# parser benchmarks
bench-parser: ## benchmark parser-only path on asmTests fixtures
	@python scripts/profile_parser.py asmTests \
		--engine $${MASM2C_PARSER_ENGINE:-postlex} \
		--target-seconds $${PARSER_BENCH_TARGET_SECONDS:-60} \
		$(if $(PARSER_BENCH_RUNS),--runs $(PARSER_BENCH_RUNS),) \
		--max-runs $${PARSER_BENCH_MAX_RUNS:-500} \
		--warmup $${PARSER_BENCH_WARMUP:-1} \
		$(if $(PARSER_BENCH_PROFILE),--profile $(PARSER_BENCH_PROFILE),) \
		$(if $(PARSER_BENCH_QUIET),--quiet,)

bench-parser-postlex: ## benchmark parser-only path with postlex engine
	@$(MAKE) bench-parser MASM2C_PARSER_ENGINE=postlex PARSER_BENCH_QUIET=$(PARSER_BENCH_QUIET)

bench-parser-cython: ## benchmark parser-only path with cython engine
	@$(MAKE) bench-parser MASM2C_PARSER_ENGINE=cython PARSER_BENCH_QUIET=$(PARSER_BENCH_QUIET)

bench-parser-compare: ## compare postlex and cython parser-only timings
	@echo "duration=$${PARSER_BENCH_TARGET_SECONDS:-60}s"; \
	postlex_tmp=$$(mktemp); cython_tmp=$$(mktemp); \
	PARSER_BENCH_QUIET=$${PARSER_BENCH_QUIET} MASM2C_PARSER_ENGINE=postlex \
		PARSER_BENCH_TARGET_SECONDS=$${PARSER_BENCH_TARGET_SECONDS:-60} \
		PARSER_BENCH_MAX_RUNS=$${PARSER_BENCH_MAX_RUNS:-500} \
		python scripts/profile_parser.py asmTests --engine postlex --target-seconds $${PARSER_BENCH_TARGET_SECONDS:-60} \
		--max-runs $${PARSER_BENCH_MAX_RUNS:-500} --warmup $${PARSER_BENCH_WARMUP:-1} --quiet > $$postlex_tmp; \
	PARSER_BENCH_QUIET=$${PARSER_BENCH_QUIET} MASM2C_PARSER_ENGINE=cython \
		PARSER_BENCH_TARGET_SECONDS=$${PARSER_BENCH_TARGET_SECONDS:-60} \
		PARSER_BENCH_MAX_RUNS=$${PARSER_BENCH_MAX_RUNS:-500} \
		python scripts/profile_parser.py asmTests --engine cython --target-seconds $${PARSER_BENCH_TARGET_SECONDS:-60} \
		--max-runs $${PARSER_BENCH_MAX_RUNS:-500} --warmup $${PARSER_BENCH_WARMUP:-1} --quiet > $$cython_tmp; \
	echo "postlex: $$(grep '^runs=' $$postlex_tmp)"; \
	echo "cython : $$(grep '^runs=' $$cython_tmp)"; \
	rm -f $$postlex_tmp $$cython_tmp

TESTS = test_insn_tests

test_insn_tests: test_insn_tests.cpp asm.h asm_16.h asm.cpp
	$(CXX) $(CXXFLAGS) -I./include -isystem /usr/local/include -Wno-overflow \
	-L/usr/local/lib -lpthread -lgtest_main \
	-o $@ $<
