from django.db import models

class Korisnik(models.Model):
    idkor = models.IntegerField(db_column='IDKor', primary_key=True)  # Field name made lowercase.
    jmbg = models.CharField(db_column='JMBG', unique=True, max_length=13)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=320)  # Field name made lowercase.
    ime = models.CharField(db_column='Ime', max_length=20)  # Field name made lowercase.
    prezime = models.CharField(db_column='Prezime', max_length=20)  # Field name made lowercase.
    lozinka = models.CharField(db_column='Lozinka', max_length=20)  # Field name made lowercase.
    vip = models.IntegerField(db_column='VIP', blank=True, null=True)  # Field name made lowercase.
    kartica = models.CharField(db_column='Kartica', max_length=30, blank=True, null=True)  # Field name made lowercase.
    stanje = models.FloatField(db_column='Stanje', blank=True, null=True)  # Field name made lowercase.
    korisnickoime = models.CharField(db_column='KorisnickoIme', unique=True, max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'korisnik'

    def __str__(self):
        return f"id: {self.idkor}, username: {self.ime}"
