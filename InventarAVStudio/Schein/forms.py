from django.forms import ModelForm
from Schein.models import Ausleihschein

class ScheinForm(ModelForm):
	class Meta:
		model = Ausleihschein
		exclude = ('issue_user', 'return_user', 'geraete', 'schein')
