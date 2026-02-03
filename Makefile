install:
	pip install -e .

test:
	pytest

lint:
	ruff check .

format:
	black .

docker-build:
	docker build -t automation-toolkit:latest .

docker-run-example:
	docker run --rm -v $(PWD)/data:/data automation-toolkit:latest validate --input /data/sample_candidates.csv
