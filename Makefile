all: 
	python3 -m venv letterboxd_env
	. letterboxd_env/bin/activate && \
	python -m pip install --upgrade pip && \
	pip install -r requirements.txt
