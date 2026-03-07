from dataclasses import dataclass


@dataclass
class ScaleUser:

    id: int
    age: int
    height: float
    gender: str
    unit: str = "kg"

    def is_male(self):
        return self.gender.lower() == "male"
