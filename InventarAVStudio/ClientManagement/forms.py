from django.forms import ModelForm
from ClientManagement.models import ComputerType, WindowsKey, Computer

class ComputerTypeForm(ModelForm):
	class Meta:
		model = ComputerType

class WindowsKeyForm(ModelForm):
	class Meta:
		model = WindowsKey

class ComputerForm(ModelForm):
	class Meta:
		model = Computer
		#exclude = ('windows_key')

