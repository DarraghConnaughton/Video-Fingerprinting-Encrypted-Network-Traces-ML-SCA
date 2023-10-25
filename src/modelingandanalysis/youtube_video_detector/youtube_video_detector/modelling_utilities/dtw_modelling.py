"""
Fiunctions for Dynamic Time Warping modelling.
"""

__author__ = "Deborah Djon"
__copyright__ = "Copyright (c) Deborah Djon, 2023"
__license__ = "MIT License"

from typing import List, Tuple
from dtw import dtw


def get_distance(reference_sequence: List[float], query_sequence: List[float])->float:
    """
    Measure similarity using DTW.
    @param reference_sequence: fingerprint.
    @param query_seqence: sequence to compare the reference sequence to.
    """
    alignment = dtw(query_sequence, 
                reference_sequence, 
                keep_internals=True,
                step_pattern="asymmetric",
                open_end=True,
                open_begin=True)
    return(alignment.normalizedDistance)

def match(fingerprints:List[int], query_sequence: List[int], distance_threshold: List[int]) -> Tuple[str, object]:
    """
    Match query sequence with one of the created sequences. 
    @param fingerprints: references to compare the query sequence to. 
    @param query sequence: sequence to match. 
    @param:  similarity treshold above which the match must be.
    """
    distances={ 
                video_id: get_distance(reference_sequence = fingerprint, 
                                            query_sequence=query_sequence) 
                for video_id, fingerprint in fingerprints.items()
    }

    min_key = min(distances, key=distances.get)

    if distances[min_key] < distance_threshold:
        return min_key, distances
    else: return None

