from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class ImpactRecord:
    """
    Represents a completed SDG challenge action.

    These fields are what get hashed — so they must be:
    - Stable (no changing values after creation)
    - Pseudonymous (no real names or emails)
    - Deterministic (timestamps in UTC ISO-8601)
    """

    user_id: str                  

    challenge_id: str             
    challenge_number: int         
    challenge_title: str          

    sdg_id: str                   
    sdg_number: int               
    target_id: str                
    indicator_id: str             

    completed_at: str             
    quantity: float          
    unit: str                    
    impact_description: str      

    location: str               
    latitude: float             
    longitude: float              

    proof_url: str               
    evidence_post_ids: list       

    difficulty: str             
    points: int                   
    schema_version: str = "1.0"

    def to_dict(self) -> dict:
        """
        Convert the ImpactRecord to a plain dictionary.
        This is the raw data before canonicalization.

        Field order here doesn't matter — canonicalization sorts keys alphabetically.
        """
        return {
            "schema_version": self.schema_version,
            # Identity
            "user_id": self.user_id,
            # Challenge
            "challenge_id": self.challenge_id,
            "challenge_number": self.challenge_number,
            "challenge_title": self.challenge_title,
            # SDG mapping
            "sdg_id": self.sdg_id,
            "sdg_number": self.sdg_number,
            "target_id": self.target_id,
            "indicator_id": self.indicator_id,
            # Completion
            "completed_at": self.completed_at,
            "quantity": self.quantity,
            "unit": self.unit,
            "impact_description": self.impact_description,
            # Location
            "location": self.location,
            "latitude": self.latitude,
            "longitude": self.longitude,
            # Evidence (file references only — never actual files)
            "proof_url": self.proof_url,
            "evidence_post_ids": self.evidence_post_ids,
            # Challenge metadata
            "difficulty": self.difficulty,
            "points": self.points,
        }

