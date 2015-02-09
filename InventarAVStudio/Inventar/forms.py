from django.forms import ModelForm
from Inventar.models import Geraet, GeraeteTyp

class CreateGeraeteTypForm(ModelForm):
	class Meta:
		model = GeraeteTyp

class GeraetForm(ModelForm):
	class Meta:
		model = Geraet
		exclude = ('schein',)
