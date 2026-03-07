from dataclasses import dataclass
from datetime import datetime


@dataclass
class ScaleMeasurement:

    user_id: int
    weight: float
    fat: float | None = None
    water: float | None = None
    muscle: float | None = None
    bone: float | None = None
    resistance1: int | None = None
    resistance2: int | None = None

    timestamp: datetime = datetime.now()
