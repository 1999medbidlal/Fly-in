install:
	@pip install flake8
	@pip install mypy
run: install
	@python3 main.py maps/challenger/01_the_impossible_dream.txt
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