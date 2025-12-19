"""Client for working with TheCatAPI"""

import random
import requests
import logging
from typing import Dict, Any, List, Tuple

import config

logger = logging.getLogger(__name__)



class CatAPIClient:
    """Client for working with TheCatAPI"""

    def __init__(self):
        self.headers = {"x-api-key": config.API_KEY}

    def fetch_breeds(self) -> List[Dict[str, Any]]:
        """Получить список пород с TheCatAPI"""
        try:
            response = requests.get(
                config.CAT_API_URL,
                headers=self.headers,
                timeout=15
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as exc:
            logger.error("Error fetching breeds: %s", exc)
            return []

    def fetch_cat_fact(self) -> str:
        """Get a random fact about cats"""

        try:
            response = requests.get(config.CAT_FACT_URL, timeout=10)
            response.raise_for_status()
            return response.json().get("fact", "No fact available.")
        except requests.RequestException as exc:
            logger.error("Error fetching cat fact: %s", exc)
            return "Couldn't fetch a fact right now."

    @staticmethod
    def get_breed_info(breed: Dict[str, Any]) -> Tuple[str, str, str]:
        """Get formatted information about the breed"""
        name = breed["name"]
        desc = breed.get("description", "")
        temp = breed.get("temperament", "")
        life = breed.get("life_span", "")
        origin = breed.get("origin", "")
        wiki = breed.get("wikipedia_url", "")

        text = f"{desc}\n\nTemperament: {temp}\nLife span: {life} years\nOrigin: {origin}"
        if wiki:
            text += f"\n\nMore info: {wiki}"

        image_url = breed.get("image", {}).get("url")
        if not image_url:
            image_url = f"https://cataas.com/cat?{random.randint(1, 10000000)}"

        return name, text, image_url


# Client instance for use in other modules
cat_api_client = CatAPIClient()