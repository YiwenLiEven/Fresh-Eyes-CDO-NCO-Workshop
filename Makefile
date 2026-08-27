.PHONY: help setup demo-data real-data workflows test all clean

help:
	@echo "make setup       Install the Python package"
	@echo "make demo-data   Generate the deterministic offline teaching dataset"
	@echo "make real-data   Fetch a lightweight teaching sample of ACCESS-CM2"
	@echo "make workflows   Run CDO, NCO, Python, validation, and plotting"
	@echo "make test        Run scientific-equivalence tests"
	@echo "make all         Run demo-data, workflows, and tests"

setup:
	python -m pip install -e .

demo-data:
	python scripts/generate_demo_data.py --output data/demo/tas_demo.nc

real-data:
	bash scripts/fetch_access_cm2_sample.sh

workflows:
	bash scripts/run_all.sh data/demo/tas_demo.nc outputs/demo

test:
	pytest -q

all: demo-data workflows test

clean:
	rm -rf data/demo data/raw data/work outputs/demo .pytest_cache __pycache__

