from django.db import models

class Benutzer(models.Model):
	vorname = models.CharField(max_length=50)
	nachname = models.CharField(max_length=50)
	telefon = models.CharField(max_length=20, blank=True)
	email = models.EmailField(blank=True)
	anschrift = models.TextField(blank=True)
	status = models.CharField(max_length=30, blank=True)
	raum = models.CharField(max_length=30, blank=True)
	haustel = models.CharField(max_length=20, blank=True)
	kommentar = models.TextField(blank=True)

	def __unicode__(self):
		return self.nachname + ', ' + self.vorname


