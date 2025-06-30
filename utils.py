import requests
import json
from typing import List, Dict
from config import API_URL, API_KEY, get_logger

logger = get_logger(__name__)


def get_collection_ids(
    collection_names: List[str], api_url: str = API_URL, api_key: str = API_KEY
) -> List[Dict[str, any]]:
    """
    Get collections ids from ALBERT API.

    Args:
        collection_names (List[str]): Collections names to search
        api_key (str): API key for authentification

    Returns:
        List[Dict[str, any]]: List of dictionaries with the keys "collection_name" and "id"

    Raises:
        requests.RequestException: In the event of an error during the HTTP request
        ValueError: In the event of a parsing error of the JSON response
    """
    url = f"{api_url}/collections"
    headers = {"accept": "application/json", "Authorization": f"Bearer {api_key}"}
    params = {"offset": 0, "limit": 15}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        data = response.json()

        ids = []
        found_names = []
        # Browse collections
        for collection in data.get("data", []):
            collection_name = collection.get("name")
            if collection_name in collection_names:
                ids.append(collection.get("id"))
                found_names.append(collection.get("name"))
        not_found = [name for name in collection_names if name not in found_names]

        if not_found:
            logger.error(f"Collections not found: {not_found}")

        return ids

    except requests.RequestException as e:
        logger.error(f"Error during HTTP request: {e}")
        raise
    except ValueError as e:
        logger.error(f"Error during JSON parsing: {e}")
        raise


def create_collection_dict(config_file_path: str):
    """
    Create a dictionary with all Albert API's collections ID based on the configuration file.

    Args:
        config_file_path (str): Path to the configuration file

    Returns:
        Dict[str, any]: Dictionary containing the configuration data
    """
    with open(config_file_path, "r", encoding="utf-8") as file:
        config_data = json.load(file)

    for collection, attributes in config_data.items():
        collection_id = get_collection_ids([collection])
        if not collection_id:
            logger.error(f"Collection '{collection}' not found. ID: None")
            config_data[collection]["id"] = None
            continue
        else:
            config_data[collection]["id"] = collection_id[0]
        logger.info(f"Collection '{collection}' found with ID: {collection_id[0]}")

    with open("data/data_gouv_search_collections.json", "w", encoding="utf-8") as file:
        json.dump(config_data, file, ensure_ascii=False, indent=4)

    logger.info("Configuration file updated with collection IDs.")
