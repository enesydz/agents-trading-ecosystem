.PHONY: setup dev-up dev-down lint test clean

setup:
	bash scripts/setup.sh

dev-up:
	bash scripts/dev-up.sh

dev-down:
	bash scripts/dev-down.sh

lint:
	bash scripts/lint.sh

test:
	bash scripts/test.sh

clean:
	docker compose -f infrastructure/docker/docker-compose.yml down -v
	rm -rf .venv **/__pycache__ **/.pytest_cache **/.mypy_cache
