# Geneweaver 3 API

Description: The API for the Geneweaver v3 application ecosystem.

## Setup

### Local

#### Requirements

- Python Poetry
- Python 3.9 or higher
- A connection to a copy of the Geneweaver Database

#### Setup

1. Clone the repository
2. Run `poetry install` in project root to install dependencies
3. Configure environment settings with environment variables or a `.env` file.
4. Run the application

To run the app execute either `uvicorn geneweaver.api.main:app --reload` with the poetry
virtualenv activated, or just run `poetry run uvicorn geneweaver.api.main:app --reload`.

This will host the application on `http://127.0.0.1:8000/` which means the swagger docs
page is available at `http://127.0.0.1:8000/docs`.
