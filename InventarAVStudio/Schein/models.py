#coding: utf8 
from django.db import models
from Benutzer.models import Benutzer
from django.contrib.auth.models import User
from Schein.overwriteStorage import OverwriteStorage

class Ausleihschein(models.Model):
	PENDING, BORROWED, RETURNED = range(3)

	STATUSES = (
		(PENDING, 'in Vorbereitung'),
		(BORROWED, 'ausgeliehen'),
		(RETURNED, 'zurückgebracht'),
	)

	issue_user = models.ForeignKey(User,null=True, related_name='issue')
	return_user = models.ForeignKey(User,null=True, blank=True, related_name='return')
	benutzer = models.ForeignKey(Benutzer,null=True)
	geraete = models.TextField(null=True)
	begin_date = models.DateField(null=True)
	end_date = models.DateField(null=True)
	schein = models.FileField(upload_to="scheine/", null=True, storage=OverwriteStorage())
	status = models.IntegerField(default=PENDING, choices=STATUSES)

	def __unicode__(self):
		return str(self.id) + ": " + self.benutzer.vorname + " " +  self.benutzer.nachname
