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

    # BMI
        self.bmi = weight / (height_m ** 2)

    # impedance index
        self.impedance_index = (self.height ** 2) / resistance

    # total body water estimation
        if self.sex == "male":
            self.tbw = (0.372 * self.impedance_index) + (0.142 * weight) + 0.069
        else:
            self.tbw = (0.356 * self.impedance_index) + (0.111 * weight) + 0.107

        self.hydration = (self.tbw / weight) * 100

    # lean mass
        self.lean_mass = self.tbw / 0.73

    # body fat mass
        self.fat_mass = weight - self.lean_mass
        self.body_fat = (self.fat_mass / weight) * 100

        self.muscle_mass = self.lean_mass * 0.55

        self.skeletal_muscle = (self.muscle_mass / weight) * 100

        self.bone_mass = weight * 0.04

        self.subcutaneous_fat = self.body_fat * 0.8

        self.visceral_fat = self.body_fat * 0.1

        self.protein = self.lean_mass * 0.20

    # BMR
        if self.sex == "male":
            self.bmr = 10 * weight + 6.25 * self.height - 5 * self.age + 5
        else:
            self.bmr = 10 * weight + 6.25 * self.height - 5 * self.age - 161

        self.metabolic_age = self.calculate_metabolic_age(self.bmr)

        return {
            "BMI": round(self.bmi, 2),
            "body_fat": round(self.body_fat, 2),
            "hydration": round(self.hydration, 2),
            "muscle_mass": round(self.muscle_mass, 2),
            "skeletal_muscle": round(self.skeletal_muscle, 2),
            "bone_mass": round(self.bone_mass, 2),
            "subcutaneous_fat": round(self.subcutaneous_fat, 2),
            "visceral_fat": round(self.visceral_fat, 2),
            "protein": round(self.protein, 2),
            "BMR": int(self.bmr),
            "metabolic_age": self.metabolic_age
        }
