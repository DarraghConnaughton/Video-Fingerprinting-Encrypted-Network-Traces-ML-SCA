"""
Fiunctions for Dynamic Time Warping modelling.
"""

__author__ = "Deborah Djon"
__copyright__ = "Copyright (c) Deborah Djon, 2023"
__license__ = "MIT License"

from typing import List, Tuple
from dtw import dtw
import numpy as np
from tslearn.barycenters import dtw_barycenter_averaging

class DTW_Model():

    def __init__(self, distance_threshold:int, fingerprints:dict[str:int] ):
        self.distance_threshold = distance_threshold
        self.fingerprints = fingerprints


    def get_distance(self, reference_sequence: List[int], query_sequence: List[int])->int:
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

    def _match(self, query_sequence: List[int]) -> Tuple[str, object]:
        """
        Match query sequence with one of the created sequences. 
        @param fingerprints: references to compare the query sequence to. 
        @param query sequence: sequence to match. 
        @param:  similarity treshold above which the match must be.
        """
        distances={ 
                    video_id: self.get_distance(reference_sequence = fingerprint, 
                                                query_sequence=query_sequence) 
                    for video_id, fingerprint in self.fingerprints.items()
        }

        min_key = min(distances, key=distances.get)

        if distances[min_key] < self.distance_threshold:
            return min_key, distances
        else: return "unknown"


    def predict(self, query_sequences: List[List[int]]) -> Tuple[List[str], List[object]]:
        """
        Match query sequence with one of the created sequences. 
        @param fingerprints: references to compare the query sequence to. 
        @param query sequence: sequence to match. 
        @param:  similarity treshold above which the match must be.
        """
        predictions = []
        distances = []
        for qs in query_sequences:
            distances={ 
                        video_id: self.get_distance(reference_sequence = fingerprint, 
                                                    query_sequence=qs) 
                        for video_id, fingerprint in self.fingerprints.items()
            }

            min_key = min(distances, key=distances.get)

            if distances[min_key] < self.distance_threshold:
                predictions.append(min_key)
                distances.append(distances)
            else: 
                predictions.append("unknown")
                distances.append(np.nan)
        return predictions, distances

    def average_sequences(self, sequence: list)-> np.ndarray:
        return dtw_barycenter_averaging(sequence, max_iter=50, tol=1e-3)