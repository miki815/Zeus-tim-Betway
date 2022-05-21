from django.db import models

class Admin(models.Model):
    idkor = models.OneToOneField('Korisnik', models.DO_NOTHING, db_column='IDKor', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'admin'


class Desetunizu(models.Model):
    idkor = models.OneToOneField('Korisnik', models.DO_NOTHING, db_column='IDKor', primary_key=True)  # Field name made lowercase.
    brojpogodaka = models.IntegerField(db_column='BrojPogodaka', blank=True, null=True)  # Field name made lowercase.
    odigrano = models.CharField(db_column='Odigrano', max_length=20, blank=True, null=True)  # Field name made lowercase.
    validno = models.IntegerField(db_column='Validno', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'desetunizu'



class Igrac(models.Model):
    idkor = models.OneToOneField('Korisnik', models.DO_NOTHING, db_column='IDKor', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'igrac'


class Korisnik(models.Model):
    idkor = models.IntegerField(db_column='IDKor', primary_key=True)  # Field name made lowercase.
    korisnickoime = models.CharField(db_column='KorisnickoIme', unique=True, max_length=20, blank=True, null=True)  # Field name made lowercase.
    ime = models.CharField(db_column='Ime', max_length=20, blank=True, null=True)  # Field name made lowercase.
    prezime = models.CharField(db_column='Prezime', max_length=20, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=20, blank=True, null=True)  # Field name made lowercase.
    lozinka = models.CharField(db_column='Lozinka', max_length=20, blank=True, null=True)  # Field name made lowercase.
    jmbg = models.CharField(db_column='JMBG', unique=True, max_length=20, blank=True, null=True)  # Field name made lowercase.
    vip = models.IntegerField(db_column='VIP', blank=True, null=True)  # Field name made lowercase.
    kartica = models.CharField(db_column='Kartica', max_length=20, blank=True, null=True)  # Field name made lowercase.
    stanje = models.DecimalField(db_column='Stanje', max_digits=15, decimal_places=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'korisnik'

    def __str__(self):
        return f"{self.idkor}: {self.korisnickoime}"


class Kvoter(models.Model):
    idkor = models.OneToOneField(Korisnik, models.DO_NOTHING, db_column='IDKor', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'kvoter'


class Odigrano10Unizu(models.Model):
    idkor = models.OneToOneField(Korisnik, models.DO_NOTHING, db_column='IDKor', primary_key=True)  # Field name made lowercase.
    ishod = models.IntegerField(db_column='Ishod')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'odigrano10unizu'


class Utakmica(models.Model):
    iduta = models.IntegerField(db_column='IDUta', primary_key=True)  # Field name made lowercase.
    datumpocetka = models.DateTimeField(db_column='DatumPocetka', blank=True, null=True)  # Field name made lowercase.
    tim1 = models.CharField(db_column='Tim1', max_length=20, blank=True, null=True)  # Field name made lowercase.
    tim2 = models.CharField(db_column='Tim2', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'utakmica'

class Utakmiceunajavi(models.Model):
    iduta = models.OneToOneField(Utakmica, models.DO_NOTHING, db_column='IDUta', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'utakmiceunajavi'


class Postavljenekvote(models.Model):
    idkvo = models.CharField(db_column='IDKvo', primary_key=True, max_length=18)  # Field name made lowercase.
    iduta = models.ForeignKey(Utakmiceunajavi, models.DO_NOTHING, db_column='IDUta', blank=True, null=True)  # Field name made lowercase.
    idkor = models.ForeignKey(Kvoter, models.DO_NOTHING, db_column='IDKor', blank=True, null=True)  # Field name made lowercase.
    kvota1 = models.DecimalField(db_column='Kvota1', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    kvotax = models.DecimalField(db_column='KvotaX', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    kvota2 = models.DecimalField(db_column='Kvota2', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    kvota11 = models.DecimalField(db_column='Kvota11', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    kvota1x = models.DecimalField(db_column='Kvota1X', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    kvota12 = models.DecimalField(db_column='Kvota12', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    kvotax1 = models.DecimalField(db_column='KvotaX1', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    kvotaxx = models.DecimalField(db_column='KvotaXX', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    kvotax2 = models.DecimalField(db_column='KvotaX2', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    kvota21 = models.DecimalField(db_column='Kvota21', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    kvota2x = models.DecimalField(db_column='Kvota2X', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    kvota22 = models.DecimalField(db_column='Kvota22', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    prvigol1 = models.DecimalField(db_column='PrviGol1', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    prvigol2 = models.DecimalField(db_column='PrviGol2', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    prvigol3 = models.DecimalField(db_column='PrviGol3', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'postavljenekvote'


class Statistika(models.Model):
    idsta = models.IntegerField(db_column='IDSta', primary_key=True)  # Field name made lowercase.
    brojpogodjenih = models.IntegerField(db_column='BrojPogodjenih', blank=True, null=True)  # Field name made lowercase.
    brojpromasenih = models.IntegerField(db_column='BrojPromasenih', blank=True, null=True)  # Field name made lowercase.
    brojprimljenihpogodjenih = models.IntegerField(db_column='BrojPrimljenihPogodjenih', blank=True, null=True)  # Field name made lowercase.
    brojprimljenihpromasenih = models.IntegerField(db_column='BrojPrimljenihPromasenih', blank=True, null=True)  # Field name made lowercase.
    ukupnouplaceno = models.DecimalField(db_column='UkupnoUplaceno', max_digits=15, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    ukupnodobijeno = models.DecimalField(db_column='UkupnoDobijeno', max_digits=15, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    idkor = models.ForeignKey(Korisnik, models.DO_NOTHING, db_column='IDKor')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'statistika'


class Tiket(models.Model):
    idtik = models.AutoField(db_column='IDTik', primary_key=True)  # Field name made lowercase.
    datumuplate = models.DateField(db_column='DatumUplate', blank=True, null=True)  # Field name made lowercase.
    iznosuplate = models.DecimalField(db_column='IznosUplate', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    kvota = models.DecimalField(db_column='Kvota', max_digits=15, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    dobitak = models.DecimalField(db_column='Dobitak', max_digits=15, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    idkor = models.ForeignKey(Igrac, models.DO_NOTHING, db_column='IDKor', blank=True, null=True)  # Field name made lowercase.
    idkvo = models.ForeignKey(Kvoter, models.DO_NOTHING, db_column='IDKvo', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tiket'



class Zavrseneutakmice(models.Model):
    iduta = models.OneToOneField(Utakmica, models.DO_NOTHING, db_column='IDUta', primary_key=True)  # Field name made lowercase.
    ishod = models.IntegerField(db_column='Ishod')  # Field name made lowercase.
    poluvremekraj = models.CharField(db_column='PoluvremeKraj', max_length=3)  # Field name made lowercase.
    prvigol = models.CharField(db_column='PrviGol', max_length=1)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'zavrseneutakmice'


class Tiketdogadjaj(models.Model):
    iddog = models.AutoField(db_column='IDDog', primary_key=True)  # Field name made lowercase.
    odigrano = models.CharField(db_column='Odigrano', max_length=20, blank=True, null=True)  # Field name made lowercase.
    kvota = models.DecimalField(db_column='Kvota', max_digits=15, decimal_places=2)  # Field name made lowercase.
    ishod = models.IntegerField(db_column='Ishod', blank=True, null=True)  # Field name made lowercase.
    iduta = models.ForeignKey(Utakmiceunajavi, models.DO_NOTHING, db_column='IDUta')  # Field name made lowercase.
    idtik = models.ForeignKey(Tiket, models.DO_NOTHING, db_column='IDTik')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tiketdogadjaj'


class Utakmica10(models.Model):
    utakmica10 = models.CharField(db_column='Utakmica10', primary_key=True, max_length=100)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'utakmica10'

class Viptiket(models.Model):
    idvip = models.AutoField(db_column='IDVip', primary_key=True)  # Field name made lowercase.
    datumuplate = models.DateField(db_column='DatumUplate', blank=True, null=True)  # Field name made lowercase.
    iznosuplate = models.DecimalField(db_column='IznosUplate', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    kvota = models.DecimalField(db_column='Kvota', max_digits=15, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    dobitak = models.DecimalField(db_column='Dobitak', max_digits=15, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    idkor = models.ForeignKey(Igrac, models.DO_NOTHING, db_column='IDKor', blank=True, null=True)  # Field name made lowercase.
    idkvo = models.ForeignKey(Kvoter, models.DO_NOTHING, db_column='IDKvo', blank=True, null=True)  # Field name made lowercase.
    idtik = models.ForeignKey(Tiket, models.DO_NOTHING, db_column='IDTik', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'viptiket'

class Vipkvote(models.Model):
    idkvo = models.AutoField(db_column='IDKvo', primary_key=True)  # Field name made lowercase.
    idtik = models.ForeignKey(Tiket, models.DO_NOTHING, db_column='IDTik', blank=True, null=True)  # Field name made lowercase.
    idkor = models.ForeignKey(Kvoter, models.DO_NOTHING, db_column='IDKor', blank=True, null=True)  # Field name made lowercase.
    kvotaprolaz = models.DecimalField(db_column='KvotaProlaz', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    kvotapad = models.DecimalField(db_column='KvotaPad', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'vipkvote'
