from django.db import models

class Diseases(models.Model):
    id = models.AutoField(primary_key=True)
    disease_name = models.CharField(max_length=100)
    symptoms = models.TextField()
    precautions = models.TextField()
    prevention_methods = models.TextField()
    medication = models.TextField()

    def __str__(self):
        return self.disease_name


class Doctors(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255)
    qualification = models.CharField(max_length=255)
    experience = models.PositiveIntegerField()
    contact_number = models.CharField(max_length=15)
    email = models.EmailField()
    password = models.CharField(max_length=128, default='123')

    def __str__(self):
        return self.name

class DoctorInfo(models.Model):
    id = models.AutoField(primary_key=True)
    disease_id = models.ForeignKey(Diseases, on_delete=models.CASCADE)
    doctor_name = models.CharField(max_length=255)
    doctor_phone = models.CharField(max_length=15)
    doctor_advice = models.TextField()

    def __str__(self):
        return f"DoctorInfo for Disease ID: {self.disease_id}"