"""Логика подбора породы кошек"""

import random
import logging
from typing import Dict, Any, Tuple

from services.cat_api import cat_api_client

logger = logging.getLogger(__name__)


class BreedMatcher:
    """Cat breed selection class"""

    LEVEL_MAP = {"low": (1, 2), "medium": (3, 3), "high": (4, 5)}
    SIZE_MAP = {"small": (0, 4), "medium": (4, 7), "large": (7, 20)}

    @staticmethod
    def calculate_weight(breed: Dict[str, Any]) -> float:
        """Calculate the average weight from the breed data"""
        weight_str = breed.get("weight", {}).get("metric", "0 - 0")
        try:
            min_w, max_w = map(int, weight_str.replace(" ", "").split("-"))
            return (min_w + max_w) / 2
        except ValueError:
            return 5.0

    @staticmethod
    def get_traits(breed: Dict[str, Any]) -> tuple:
        """Extract characteristics from the breed data"""
        energy = breed.get("energy_level", 3)
        grooming_level = breed.get("grooming", 3)
        if breed.get("hairless", 0) == 1:
            grooming_level = 1
        affection = breed.get("affection_level", 3)
        child_friendly = breed.get("child_friendly", 3)
        friendliness = max(affection, child_friendly)
        shedding = breed.get("shedding_level", 3)
        vocalisation = breed.get("vocalisation", 3)
        return energy, grooming_level, friendliness, shedding, vocalisation

    def score_breed(self, breed: Dict[str, Any], prefs: Dict[str, str]) -> float:
        """Evaluate the breed based on your preferences"""
        avg_w = self.calculate_weight(breed)
        energy, grooming, friendliness, shedding, vocalisation = self.get_traits(breed)

        score = 0.0

        if (prefs.get("size") and
                self.SIZE_MAP[prefs["size"]][0] <= avg_w <= self.SIZE_MAP[prefs["size"]][1]):
            score += 2.0
        if (prefs.get("activity") and
                self.LEVEL_MAP[prefs["activity"]][0] <= energy <= self.LEVEL_MAP[prefs["activity"]][1]):
            score += 1.5
        if (prefs.get("grooming") and
                self.LEVEL_MAP[prefs["grooming"]][0] <= grooming <= self.LEVEL_MAP[prefs["grooming"]][1]):
            score += 1.5
        if (prefs.get("friendliness") and
                self.LEVEL_MAP[prefs["friendliness"]][0] <= friendliness <= self.LEVEL_MAP[prefs["friendliness"]][1]):
            score += 1.5
        if (prefs.get("shedding") and
                self.LEVEL_MAP[prefs["shedding"]][0] <= shedding <= self.LEVEL_MAP[prefs["shedding"]][1]):
            score += 1.0
        if (prefs.get("vocalization") and
                self.LEVEL_MAP[prefs["vocalization"]][0] <= vocalisation <= self.LEVEL_MAP[prefs["vocalization"]][1]):
            score += 1.0
        if breed.get("image"):
            score += 0.5

        return score

    def match_breed(self, prefs: Dict[str, str]) -> Tuple[str, str, str]:
        """Select a breed based on your preferences"""
        breeds = cat_api_client.fetch_breeds()
        if not breeds:
            return "No breed", "Unable to load breeds from API.", "https://cataas.com/cat"

        best_breed = None
        best_score = 0.0

        for breed in breeds:
            score = self.score_breed(breed, prefs)
            if score > best_score:
                best_score = score
                best_breed = breed

        if best_breed:
            return cat_api_client.get_breed_info(best_breed)

        # Fallback — a random breed
        random_breed = random.choice(breeds)
        name = random_breed["name"]
        base_text = "No perfect match found, but here's a great breed anyway!\n\n"
        text = base_text + random_breed.get("description", "")

        image_url = random_breed.get("image", {}).get("url")
        if not image_url:
            image_url = f"https://cataas.com/cat?{random.randint(1, 10000000)}"

        return name, text, image_url


# An instance of a matcher for use in other modules
breed_matcher = BreedMatcher()