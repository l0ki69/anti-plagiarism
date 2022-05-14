from typing import List, Tuple


class Uniqueness:
    """
    Class for calculating the percentage of uniqueness
    """
    @classmethod
    def uniqueness_wroker(cls, shingles: Tuple[List[str]] = None) -> float:
        if shingles is None:
            return 0.0

        uniqueness_percent = len(set(shingles[0]) & set(shingles[1])) / len(set(shingles[0]))

        return float(uniqueness_percent)