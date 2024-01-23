from django.db import models
from django.contrib.auth.models import User
  
class Raeume(models.Model):
    raumNR = models.CharField(max_length=5, primary_key=True)
    bestuhlung = models.IntegerField()
    ausstattung = models.CharField(max_length= 7, choices=[("hoch", "hoch"), ("mittel", "mittel"), ("niedrig", "niedrig")])

    def __str__(self):
       return self.raumNR  

class MyBookings(models.Model):
    buchungsNR = models.AutoField(primary_key=True)
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    raumNR = models.ForeignKey(Raeume, on_delete=models.CASCADE)
    datum = models.DateField()
    