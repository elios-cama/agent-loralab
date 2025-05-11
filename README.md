# Portfolio AI Assistant

A FastAPI backend that uses AI agents to provide information about my portfolio projects.

## Features

- PostgreSQL with pgvector for embedding storage
- FastAPI backend with AI agent integration
- Automatic knowledge base initialization on startup

## Setup

### Requirements

- Python 3.9+
- Docker (for PostgreSQL with pgvector)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/portfolio-ai.git
cd portfolio-ai
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Start the PostgreSQL database with pgvector:
```bash
docker run -d \
  -e POSTGRES_DB=ai \
  -e POSTGRES_USER=ai \
  -e POSTGRES_PASSWORD=ai \
  -e PGDATA=/var/lib/postgresql/data/pgdata \
  -v pgvolume:/var/lib/postgresql/data \
  -p 5532:5432 \
  --name pgvector \
  phidata/pgvector:16
```

4. Create a `.env` file with your configuration.

5. Run the application:
```bash
python main.py
```

## Deployment

This project is configured for deployment on Railway.

## License

MIT 