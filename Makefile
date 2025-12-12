AI_DIR := ai/

ruff:
	@echo "Running Ruff on $(AI_DIR) folder..."
	@ruff format $(AI_DIR)
	@ruff check $(AI_DIR) --fix

test:
	@echo "Running tests..."
	@PYTHONPATH=. pytest $(AI_DIR)tests/ -v

test-cov:
	@echo "Running tests with coverage..."
	@PYTHONPATH=. pytest $(AI_DIR)tests/ --cov=ai --cov-report=html --cov-report=term