
CREATE TABLE Utakmica
(
	IDUta                INTEGER NOT NULL,
	DatumPocetka         INTEGER NULL,
	Tim1                 VARCHAR(20) NULL,
	Tim2                 VARCHAR(20) NULL,
	CONSTRAINT XPKUtakmica PRIMARY KEY (IDUta)
);

CREATE TABLE ZavrseneUtakmice
(
	IDUta                INTEGER NOT NULL,
	Ishod                INTEGER NOT NULL,
	PoluvremeKraj        CHAR(3) NOT NULL,
	PrviGol              CHAR(1) NOT NULL,
	CONSTRAINT XPKZavrseneUtakmice PRIMARY KEY (IDUta),
	CONSTRAINT R_9 FOREIGN KEY (IDUta) REFERENCES Utakmica (IDUta)
		ON DELETE CASCADE
);

CREATE TABLE UtakmiceUToku
(
	IDUta                INTEGER NOT NULL,
	CONSTRAINT XPKUtakmiceUToku PRIMARY KEY (IDUta),
	CONSTRAINT R_7 FOREIGN KEY (IDUta) REFERENCES Utakmica (IDUta)
		ON DELETE CASCADE
);

CREATE TABLE Korisnik
(
	IDKor                INTEGER NOT NULL,
	KorisnickoIme        VARCHAR(20) NULL,
	Ime                  VARCHAR(20) NULL,
	Prezime              VARCHAR(20) NULL,
	Email                VARCHAR(20) NULL,
	Lozinka              VARCHAR(20) NULL,
	JMBG                 VARCHAR(20) NULL,
	VIP                  boolean NULL,
	Kartica              VARCHAR(20) NULL,
	Stanje               DECIMAL(15,2) NULL,
	CONSTRAINT XPKKorisnik PRIMARY KEY (IDKor)
);

CREATE UNIQUE INDEX XAK1Korisnik ON Korisnik
(
	JMBG ASC
);

CREATE UNIQUE INDEX XAK2Korisnik ON Korisnik
(
	KorisnickoIme ASC
);

CREATE TABLE Igrac
(
	IDKor                INTEGER NOT NULL,
	CONSTRAINT XPKIgrac PRIMARY KEY (IDKor),
	CONSTRAINT R_5 FOREIGN KEY (IDKor) REFERENCES Korisnik (IDKor)
		ON DELETE CASCADE
);

CREATE TABLE Tiket
(
	IDTik                INTEGER NOT NULL,
	DatumUplate          DATE NULL,
	IznosUplate          DECIMAL(10,2) NULL,
	Dobitak              DECIMAL(15,2) NULL,
	IDUta2               INTEGER NULL,
	IDUta3               INTEGER NULL,
	IDUta4               INTEGER NULL,
	IDUta5               INTEGER NULL,
	IDUta6               INTEGER NULL,
	IDUta7               INTEGER NULL,
	IDUta8               INTEGER NULL,
	IDUta9               INTEGER NULL,
	IDUta10              INTEGER NULL,
	IDKor                INTEGER NULL,
	IDUta1               INTEGER NOT NULL,
	CONSTRAINT XPKTiket PRIMARY KEY (IDTik),
	CONSTRAINT R_10 FOREIGN KEY (IDKor) REFERENCES Igrac (IDKor),
	CONSTRAINT R_15 FOREIGN KEY (IDUta1) REFERENCES Utakmica (IDUta),
	CONSTRAINT R_16 FOREIGN KEY (IDUta2) REFERENCES Utakmica (IDUta),
	CONSTRAINT R_18 FOREIGN KEY (IDUta3) REFERENCES Utakmica (IDUta),
	CONSTRAINT R_19 FOREIGN KEY (IDUta4) REFERENCES Utakmica (IDUta),
	CONSTRAINT R_20 FOREIGN KEY (IDUta5) REFERENCES Utakmica (IDUta),
	CONSTRAINT R_21 FOREIGN KEY (IDUta6) REFERENCES Utakmica (IDUta),
	CONSTRAINT R_22 FOREIGN KEY (IDUta7) REFERENCES Utakmica (IDUta),
	CONSTRAINT R_23 FOREIGN KEY (IDUta8) REFERENCES Utakmica (IDUta),
	CONSTRAINT R_24 FOREIGN KEY (IDUta9) REFERENCES Utakmica (IDUta),
	CONSTRAINT R_25 FOREIGN KEY (IDUta10) REFERENCES Utakmica (IDUta)
);

CREATE TABLE Statistika
(
	IDSta                INTEGER NOT NULL,
	BrojDob              INTEGER NOT NULL,
	DobijeniIznos        DECIMAL(15,2) NOT NULL,
	UkupnaUplata         DECIMAL(15,2) NOT NULL,
	IDKor                INTEGER NOT NULL,
	CONSTRAINT XPKStatistika PRIMARY KEY (IDSta),
	CONSTRAINT R_11 FOREIGN KEY (IDKor) REFERENCES Korisnik (IDKor)
);

CREATE TABLE UtakmiceUNajavi
(
	IDUta                INTEGER NOT NULL,
	CONSTRAINT XPKUtakmiceUNajavi PRIMARY KEY (IDUta),
	CONSTRAINT R_8 FOREIGN KEY (IDUta) REFERENCES Utakmica (IDUta)
		ON DELETE CASCADE
);

CREATE TABLE Kvoter
(
	IDKor                INTEGER NOT NULL,
	CONSTRAINT XPKKvoter PRIMARY KEY (IDKor),
	CONSTRAINT R_4 FOREIGN KEY (IDKor) REFERENCES Korisnik (IDKor)
		ON DELETE CASCADE
);

CREATE TABLE PostavljeneKvote
(
	IDKvo                CHAR(18) NOT NULL,
	IDUta                INTEGER NULL,
	IDKor                INTEGER NULL,
	Kvota1               DECIMAL(5,2) NULL,
	KvotaX               DECIMAL(5,2) NULL,
	Kvota2               DECIMAL(5,2) NULL,
	Kvota11              DECIMAL(5,2) NULL,
	Kvota1X              DECIMAL(5,2) NULL,
	Kvota12              DECIMAL(5,2) NULL,
	KvotaX1              DECIMAL(5,2) NULL,
	KvotaXX              DECIMAL(5,2) NULL,
	KvotaX2              DECIMAL(5,2) NULL,
	Kvota21              DECIMAL(5,2) NULL,
	Kvota2X              DECIMAL(5,2) NULL,
	Kvota22              DECIMAL(5,2) NULL,
	PrviGol1             DECIMAL(5,2) NULL,
	PrviGol2             DECIMAL(5,2) NULL,
	PrviGol3             DECIMAL(5,2) NULL,
	CONSTRAINT XPKPostavljeneKvote PRIMARY KEY (IDKvo),
	CONSTRAINT R_13 FOREIGN KEY (IDUta) REFERENCES UtakmiceUNajavi (IDUta),
	CONSTRAINT R_14 FOREIGN KEY (IDKor) REFERENCES Kvoter (IDKor)
);

CREATE TABLE Odigrano10UNizu
(
	IDKor                INTEGER NOT NULL,
	Ishod                INTEGER NOT NULL,
	CONSTRAINT XPKOdigrano10UNizu PRIMARY KEY (IDKor),
	CONSTRAINT R_1 FOREIGN KEY (IDKor) REFERENCES Korisnik (IDKor)
);

CREATE TABLE DesetUNizu
(
	IDKor                INTEGER NULL,
	RedniBroj            INTEGER NOT NULL,
	Pogodak              INTEGER NULL,
	CONSTRAINT XPKDesetUNizu PRIMARY KEY (RedniBroj),
	CONSTRAINT R_12 FOREIGN KEY (IDKor) REFERENCES Korisnik (IDKor)
);

CREATE TABLE Admin
(
	IDKor                INTEGER NOT NULL,
	CONSTRAINT XPKAdmin PRIMARY KEY (IDKor),
	CONSTRAINT R_3 FOREIGN KEY (IDKor) REFERENCES Korisnik (IDKor)
		ON DELETE CASCADE
);
