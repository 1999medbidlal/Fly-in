install:
	@pip install flake8
	@pip install mypy
run: 
	@python3 main.py maps/medium/01_dead_end_trap.txt
debug:
	@python3 -m pdb
clean:
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@rm -rf .mypy_cache .pytest_cache
lint:
	@flake8 .
	@mypy . --warn-return-any \
	       --warn-unused-ignores \
	       --ignore-missing-imports \
	       --disallow-untyped-defs \
	       --check-untyped-defs