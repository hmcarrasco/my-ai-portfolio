API_DIR := api/

ruff:
	@echo "Running Ruff on $(API_DIR) folder..."
	@ruff format $(API_DIR)
	@ruff check $(API_DIR) --fix