AI_DIR := ai/
FE_DIR := frontend/

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

fe-lint:
	@echo "Running ESLint on $(FE_DIR)..."
	@cd $(FE_DIR) && npm run lint

fe-test:
	@echo "Running frontend tests..."
	@cd $(FE_DIR) && npm test

fe-test-watch:
	@echo "Running frontend tests in watch mode..."
	@cd $(FE_DIR) && npm run test:watch