from itertools import count
from django.db import models

# Create your models here.


class VehicleType(models.Model):
    name = models.CharField(max_length=32)
    max_capacity = models.PositiveIntegerField()

    def __str__(self) -> str:
        return self.name


class Vehicle(models.Model):
    name = models.CharField(max_length=32)
    passengers = models.PositiveIntegerField()
    vehicle_type = models.ForeignKey(
        VehicleType, null=True, on_delete=models.SET_NULL)
    number_plate = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.name

    def can_start(self) -> bool:
        return self.vehicle_type.max_capacity >= self.passengers

    def get_distribution(self):
        passengers = []
        capacity = []
        count = 0
        for i in range(int(self.vehicle_type.max_capacity/2)):
            for j in range(2):
                if self.passengers > count:
                    passengers.append(True)
                    count += 1
                else:
                    passengers.append(False)
                    count += 1
            capacity.append(passengers)
            passengers = []
        return capacity

    def validate_number_plate(self, num_plate):
        num_plate = self.number_plate.split("-")
        valid = False
        for n in num_plate[0]:
            if n.isalpha():
                valid = True
        if num_plate[1].isdigit() and num_plate[2].isdigit():
            valid = True
        return valid


class Journey(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT)
    start = models.DateField()
    end = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.vehicle.name} ({self.start} - {self.end})"

    def is_finished(self):
        finish = False
        if self.end:
            finish = True
        return finish
