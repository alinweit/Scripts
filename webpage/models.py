from django.db import models


class User(models.Model):
    userID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    vorname = models.CharField(max_length=20)
    email = models.EmailField(max_length=70, unique=True)
    passwort = models.CharField(max_length=32)
    rolle = models.CharField(max_length=5, choices=[("user", "User"), ("admin", "Admin")], default='user')

    def __str__(self):
        return self.email   
    
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
    