.PHONY: all clean repo2txt-lib seed test

# Default target
all: repo2txt-lib

## 🔧 Generate repo2txt output from the library source
repo2txt-lib:
	@echo "📄 Converting files to text using repo2txt..."
	python src/repo2txt/repo2txt.py -o repo2txt-lib.txt --include-dir src/repo2txt

## 🌱 Seed the test-repo directory with test data
seed:
	@echo "🌱 Seeding test data..."
	@./seed_test_data.sh

## ✅ Run automated tests with pytest
test: seed
	@echo "🧪 Running tests..."
	pytest tests

## 🧹 Clean generated test files and output
clean:
	@echo "🧹 Cleaning test and output artifacts..."
	rm -rf test-repo
	rm -f repo2txt-lib.txt
	rm -rf __pycache__ .pytest_cache .mypy_cache
	find tests/tmp -type f -name '*.txt' -delete || true
	find tests/tmp -type d -empty -delete || true
