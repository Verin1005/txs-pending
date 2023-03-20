# Setup

    pip install -r requirements.txt

# Install Chrome Browser

# Run

    uvicorn main:app --host <HOST> --port <PORT>

# Docs

    http://127.0.0.1:8000/redoc
# Docker

	docker build -t <name>:<tag> .
	docker run --name txpending --rm -p 3000:3000 <image>
