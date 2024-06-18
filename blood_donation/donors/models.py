from django.db import models
from django.core.validators import MinValueValidator
from datetime import date


BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    

class Donor(models.Model):
    
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    weight = models.FloatField(validators=[MinValueValidator(50)])
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    location = models.CharField(max_length=100)
    disease = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=15, blank= True)  # Added phone number field
    

    def age(self):
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )

    def is_eligible(self):
        return self.age() >= 18 and self.weight >= 50 and not self.disease

class BloodBank(models.Model):
    
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    quantity = models.IntegerField(default=0)
    


    def __str__(self):
        return self.name

class BloodGroup(models.Model):
    blood_bank = models.ForeignKey(BloodBank, on_delete=models.CASCADE)
    blood_group_name = models.CharField(max_length=10, choices=BLOOD_GROUP_CHOICES)
    quantity_available = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.blood_group_name} - {self.blood_bank}"
        
class Donation(models.Model):
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
    blood_bank = models.ForeignKey(BloodBank, on_delete=models.CASCADE)
    units_donated = models.IntegerField()
    date = models.DateField(auto_now_add=True)        