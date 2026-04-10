.PHONY: setup pipeline dashboard clean

# Install dependencies
setup:
	pip install --upgrade pip
	pip install -r requirements.txt


# Run full pipeline
pipeline:
	python load_data.py
	python cell_analysis.py >> results.txt


# Launch dashboard
dashboard:
	streamlit run dashboard.py


# Optional cleanup
clean:
	rm -f teiko.db
	rm -f *.pyc
	rm -rf __pycache__
	rm -f *.html
	rm -f *.png
	rm -f results.txt
