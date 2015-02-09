from django.forms import ModelForm
from Benutzer.models import Benutzer

class UserForm(ModelForm):
	class Meta:
		model = Benutzer
