from django.db import models

class DashboardCategory(models.Model):
	name = models.CharField(max_length=50)

	def __unicode__(self):
		return self.name

class DashboardEntry(models.Model):
	name = models.CharField(max_length=100)
	link = models.URLField(max_length=200, blank=True)
	description = models.TextField(blank=True)
	category = models.ForeignKey(DashboardCategory)

	def __unicode__(self):
		return self.name
	
