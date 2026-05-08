.PHONY: install run clean

install:
	uv sync

run:
	uv run streamlit run app.py

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete