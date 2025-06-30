# Albert Data Collections

Useful functionalities and pipelines related to ALBERT's data collections.

## Installation

Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

Install dependencies:
```bash
pip install -r pyproject.toml
```

## Configuration

Create a `.env` file in the project root with the required environment variables. You can use the example file as a template:

```bash
cp .env.example .env
```

Then edit the `.env` file with your actual values.

## Usage

Update collections dictionary:
```bash
python main.py update_collections_dict
```
