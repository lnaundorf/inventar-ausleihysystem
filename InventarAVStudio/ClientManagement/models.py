from django.db import models

class ComputerType(models.Model):	
	vendor = models.CharField(max_length=50, verbose_name="Hersteller")
	name = models.CharField(max_length=50, verbose_name="Name")
	url = models.URLField(max_length=200,blank=True, verbose_name="Hersteller Webseite")
	description = models.TextField(blank=True, verbose_name="Beschreibung")

	def __unicode__(self):
		return self.vendor + " " + self.name

class WindowsKey(models.Model):
	WIN_XP, WIN_VISTA, WIN_7, WIN_8, WIN_SERVER_2003, WIN_SERVER_2008, WIN_SERVER_2008_R2, WIN_SERVER_2012 = range(8)

	OS_MAJOR_TYPES = (
		(WIN_XP, 'Windows XP'),
		(WIN_VISTA, 'Windows Vista'),
		(WIN_7, 'Windows 7'),
		(WIN_8, 'Windows 8'),
		(WIN_SERVER_2003, 'Windows Server 2003'),
		(WIN_SERVER_2008, 'Windows Server 2008'),
		(WIN_SERVER_2008_R2, 'Windows Server 2008 R2'),
		(WIN_SERVER_2012, 'Windows Server 2012'),
	)

	OS_MAJOR_TYPES_SHORT = (
		(WIN_XP, 'WinXP'),
		(WIN_VISTA, 'WinVista'),
		(WIN_7, 'Win7'),
		(WIN_8, 'Win8'),
		(WIN_SERVER_2003, 'Windows Server 2003'),
		(WIN_SERVER_2008, 'Windows Server 2008'),
		(WIN_SERVER_2008_R2, 'Windows Server 2008 R2'),
		(WIN_SERVER_2012, 'Windows Server 2012'),
	)

	HOME_BASIC, HOME_PREMIUM, PROFESSIONAL, ULTIMATE = range(4)

	OS_MINOR_TYPES = (
		(HOME_BASIC, 'Home Basic'),
		(HOME_PREMIUM, 'Home Premium'),
		(PROFESSIONAL, 'Professional'),
		(ULTIMATE, 'Ultimate'),
	)

	OS_MINOR_TYPES_SHORT = (
		(HOME_BASIC, 'Home Bas.'),
		(HOME_PREMIUM, 'Home Prem.'),
		(PROFESSIONAL, 'Pro'),
		(ULTIMATE, 'Ult'),
	)

	X86, X64 = range(2)

	BIT_TYPES = (
		(X86, 'x86'),
		(X64, 'x64'),
	)

	OS_major_type = models.IntegerField(default=WIN_7, choices=OS_MAJOR_TYPES, blank=True)
	OS_minor_type = models.IntegerField(default=PROFESSIONAL, choices=OS_MINOR_TYPES, blank=True)
	bit_type = models.IntegerField(default=X64, choices=BIT_TYPES, blank=True)
	key = models.CharField(max_length=50)

	def __unicode__(self):
		return WindowsKey.OS_MAJOR_TYPES_SHORT[self.OS_major_type][1] + " " + WindowsKey.OS_MINOR_TYPES_SHORT[self.OS_minor_type][1] + " " + WindowsKey.BIT_TYPES[self.bit_type][1] + ": " + self.key

	def short_name(self):
		return WindowsKey.OS_MAJOR_TYPES[self.OS_major_type][1] + " " + WindowsKey.OS_MINOR_TYPES[self.OS_minor_type][1] + " " + WindowsKey.BIT_TYPES[self.bit_type][1]

	def name(self):
		return WindowsKey.OS_MAJOR_TYPES[self.OS_major_type][1] + " " + WindowsKey.OS_MINOR_TYPES[self.OS_minor_type][1]

	def bit_string(self):
		return WindowsKey.BIT_TYPES[self.bit_type][1]
	
class Computer(models.Model):
	type = models.ForeignKey(ComputerType, verbose_name="Computertyp")
	serial_number = models.CharField(max_length=50, blank=True, verbose_name="Seriennummer")
	room = models.CharField(max_length=50, blank=True, verbose_name="Raum")
	name = models.CharField(max_length=50, blank=True, verbose_name="Computername")
	ip_address = models.IPAddressField(blank=True, verbose_name="IP-Adresse")
	mac_address = models.CharField(max_length=20, blank=True, verbose_name="MAC-Adresse")
	windows_key = models.OneToOneField(WindowsKey, blank=True, null=True, verbose_name="Windows Key")
	comment = models.TextField(blank=True, verbose_name="Kommentar")

	def __unicode__(self):
		return self.name



