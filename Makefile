.PHONY: setup serve upload process

setup:
	@echo "Installing dependencies..."
	pip install -r requirements.txt
	@echo "Downloading Ollama..."
	wget https://github.com/ollama_org/ollama/releases/download/v0.0.8/ollama_0.0.8_Linux_x86_64.tar.gz
	@echo "Extracting Ollama..."
	tar -xvf ollama_0.0.8_Linux_x86_64.tar.gz
	@echo "Creating source_documents directory..."
	mkdir -p source_documents

serve:
	@echo "Starting Ollama..."
	ollama serve 

upload:
	@echo "Starting Uploader server..."
	python3 uploader.py

process:
	@echo "Starting ingest.py and privateGPT.py scripts..."
	python3 ingest.py && python3 privateGPT.py