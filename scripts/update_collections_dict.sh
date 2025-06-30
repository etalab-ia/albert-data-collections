#!/bin/bash

# Load environment variables from .env file
export $(grep -v '^#' .env | xargs)


# Run the Python script
python3 main.py update_collections_dict