# Geneweaver 3 API

[![GitHub deployments](https://img.shields.io/github/deployments/thejacksonlaboratory/geneweaver-api/jax-cluster-prod-10--prod?style=for-the-badge&label=Deployment%20Status)](https://geneweaver.jax.org/aon/api/docs)
[![Website](https://img.shields.io/website?url=https%3A%2F%2Fgeneweaver.jax.org%2Fapi%2Fdocs&up_message=available&down_message=down&style=for-the-badge&logo=swagger&label=Swagger%20Page&link=https%3A%2F%2Fgeneweaver.jax.org%2Fapi%2Fdocs)](https://geneweaver.jax.org/api/docs)
[![Website](https://img.shields.io/website?url=https%3A%2F%2Fthejacksonlaboratory.github.io%2Fgeneweaver-docs%2F&up_message=AVAILABLE&style=for-the-badge&logo=materialformkdocs&label=Documentation)](https://thejacksonlaboratory.github.io/geneweaver-docs/)

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

### Code linters

Ruff rules: (https://docs.astral.sh/ruff/rules/)

From active local environment on command line run:

    ruff src/ tests/ --fix

then run black (code formatter: https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html)

    black src/ tests/

### Unit test

Create appropriate test per code modifications without dependencies to external resources 
such as DB, Webserver, or APIs. Create appropriate mocks for external resources and data as needed.

    Tests directory: geneweaver-api/tests

To execute tests, from the command line run:

    pytest tests --cov=geneweaver.api --cov-report term  --cov-report html 

### Continuous Integration & Deployment
When a PR is crated in GitHub, it will automatically trigger a workflow that will run 
the tests and build the docker images, and then deploy to `dev`. Please be aware of this
when creating tests in order to avoid conflicts with other PRs.

When a PR is merged into `main`, it will automatically trigger a workflow that will run
the tests and build the docker images, and then deploy to `sqa`.

In order for any deployment to run, other than to `dev`, two things must be true:
    - the deployment must be approved by SQA.
    - the version number in `pyproject.toml` must be incremented.

In order for the `stage` and `prod` deployments to run, the version number in 
`pyproject.toml` must not contain a letter. This indicates that it is a release version.

#### Version Numbers
When creating a bugfix or feature addition PR, it is required that your version number
contains a letter. This indicates to SQA that the code needs to be tests before it is 
released. 

For example, if the current version is `0.1.0`, then your PR should increment
the version number to `0.1.1a0` when creating a bugfix PR. The SQA team will then
test your code in the `sqa` environment. 

If the code passes SQA testing, they will inform you that `0.1.1a0` has passed QA, at 
which point you should create a PR with a single line change that increments the version
number to `0.1.1`.

If `0.1.1a0` fails QA, then you will need to create a fix, and increment the version
number to `0.1.1a1`. This process will continue until the code passes QA, at which
point you will increment the version number to `0.1.1` and create a PR to merge into
