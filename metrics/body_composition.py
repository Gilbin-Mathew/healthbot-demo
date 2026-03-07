import math

class BodyCompositionCalculator:

    def __init__(self, height_cm, age, sex):
        self.height = height_cm
        self.age = age
        self.sex = sex.lower()

    def calculate_metabolic_age(self, bmr):

        male_table = {
            18:1720,20:1690,25:1670,30:1640,
            35:1610,40:1580,45:1550,50:1500,
            55:1460,60:1420
        }

        female_table = {
            18:1500,20:1480,25:1460,30:1430,
            35:1400,40:1370,45:1340,50:1300,
            55:1270,60:1240
        }

        table = male_table if self.sex == "male" else female_table

        return min(table.keys(), key=lambda age: abs(table[age] - bmr))

    def calculate(self, weight, resistance):

        height_m = self.height / 100

        bmi = weight / (height_m ** 2)

        if self.sex == "male":
            body_fat = (1.20 * bmi) + (0.23 * self.age) - 16.2
        else:
            body_fat = (1.20 * bmi) + (0.23 * self.age) - 5.4

        body_fat = max(5, min(body_fat, 50))

        hydration = 100 - body_fat
        lean_mass = weight * (1 - body_fat/100)

        muscle_mass = lean_mass * 0.55
        skeletal_muscle = (muscle_mass / weight) * 100

        bone_mass = weight * 0.04

        subcutaneous_fat = body_fat * 0.8
        visceral_fat = body_fat * 0.1

        protein = lean_mass * 0.20

        if self.sex == "male":
            bmr = 10*weight + 6.25*self.height - 5*self.age + 5
        else:
            bmr = 10*weight + 6.25*self.height - 5*self.age - 161

        metabolic_age = self.calculate_metabolic_age(bmr)

        return {
            "BMI": round(bmi,2),
            "body_fat": round(body_fat,2),
            "hydration": round(hydration,2),
            "muscle_mass": round(muscle_mass,2),
            "skeletal_muscle": round(skeletal_muscle,2),
            "bone_mass": round(bone_mass,2),
            "subcutaneous_fat": round(subcutaneous_fat,2),
            "visceral_fat": round(visceral_fat,2),
            "protein": round(protein,2),
            "BMR": int(bmr),
            "metabolic_age": metabolic_age
        }
