#!/usr/bin/env python3

"""
Albert Data Collections CLI.

Usage:
    main.py update_collections_dict [--config-file=<path>]
    main.py (-h | --help)

Commands:
    update_collections_dict <config_file_path>  Update the collections dictionary from the given configuration file path.

Options:
    --config-file=<path> Path to the configuration file [default: config/data_gouv_search_config.json].

Examples:
    main.py update_collections_dict
    main.py update_collections_dict --config-file=config/data_gouv_search_config.json
"""
import sys
from docopt import docopt
from config import setup_logging, get_logger
from utils import create_collection_dict

# Setup logging at the start
setup_logging()
logger = get_logger(__name__)


def main():
    try:
        args = docopt(__doc__)

        if args["update_collections_dict"]:
            config_file_path = args["--config-file"] if args["--config-file"] else "config/data_gouv_search_config.json"
            logger.info(f"Updating collections dictionary from {config_file_path}")
            create_collection_dict(config_file_path=config_file_path)
            logger.info("Collections dictionary updated successfully.")

        return 0
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)