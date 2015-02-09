#coding: utf8 
from django.db import models
from Schein.models import Ausleihschein

class GeraeteTyp(models.Model):
	name = models.CharField(max_length=50)

	def __unicode__(self):
		return self.name

class Geraet(models.Model):
	AVAILABLE, PENDING, BORROWED, BLOCKED = range(4)

	STATUSES = (
		(AVAILABLE, 'Verfügbar'),
		(PENDING, 'Auf Ausleihschein'),
		(BORROWED, 'ausgeliehen'),
		(BLOCKED, 'nicht ausleihbar / blockiert'),
	)

	nummer = models.CharField(max_length=10, blank=True)
	typ = models.ForeignKey(GeraeteTyp, null=True, blank=True)
	name = models.CharField(max_length=100)
	kommentar = models.TextField(max_length=200, blank=True)
	ort = models.CharField(max_length=100, blank=True)
	status = models.IntegerField(default=AVAILABLE, choices=STATUSES)
	schein = models.ForeignKey(Ausleihschein, null=True, blank=True)

	def __unicode__(self):
		return self.nummer + ": " + self.name

