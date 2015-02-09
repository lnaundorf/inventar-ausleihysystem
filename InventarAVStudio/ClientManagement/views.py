from django.shortcuts import render_to_response, redirect
from Inventar.models import Geraet, GeraeteTyp
from django.db.models import Q
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from ClientManagement.models import ComputerType, WindowsKey, Computer
from ClientManagement.forms import ComputerTypeForm, WindowsKeyForm, ComputerForm
from django.contrib import messages
import re

@login_required
def index(request):
	computers = Computer.objects.all().order_by('name')
	types = ComputerType.objects.all().order_by('vendor', 'name')
	keys = WindowsKey.objects.all()
	
	return render_to_response('clientmanagement/index.html', {'computers': computers, 'types': types, 'keys': keys, 'active': 'clientManagement'}, context_instance=RequestContext(request))

@login_required
def computer_edit(request, id):
	try:
		c = Computer.objects.get(pk=id)
	except Computer.DoesNotExist:
			return render_to_response('clientmanagement/404.html')

	if request.method == 'POST':
		form = ComputerForm(request.POST, instance=c)
		if form.is_valid():
			c = form.save()
			messages.add_message(request, messages.SUCCESS, 'Der Computer "' + c.name + '" wurde erfolgreich bearbeitet.')
			return redirect('/pool/')
	else:
		form = ComputerForm(instance=c)

	return render_to_response('clientmanagement/computer_form.html', {'form': form, 'action': 'Speichern', 'active': 'clientManagement'}, context_instance=RequestContext(request))

@login_required
def computer_create(request):
	if request.method == 'POST':
		form = ComputerForm(request.POST)
		if form.is_valid():
			c = form.save()
			messages.add_message(request, messages.SUCCESS, 'Der Computer "' + c.name + '" wurde erfolgreich erstellt.')
			return redirect('/pool/')
	else:
		form = ComputerForm()

	return render_to_response('clientmanagement/computer_form.html', {'form': form, 'action': 'Erstellen', 'active': 'clientManagement'}, context_instance=RequestContext(request))

@login_required
def type_edit(request, id):
	try:
		t = ComputerType.objects.get(pk=id)
	except ComputerType.DoesNotExist:
			return render_to_response('clientmanagement/404.html')

	if request.method == 'POST':
		form = ComputerTypeForm(request.POST, instance=t)
		if form.is_valid():
			t = form.save()
			messages.add_message(request, messages.SUCCESS, 'Der Computertyp "' + t.name + '" wurde erfolgreich bearbeitet.')
			return redirect('/pool/')
	else:
		form = ComputerTypeForm(instance=t)

	return render_to_response('clientmanagement/type_form.html', {'form': form, 'action': 'Speichern', 'active': 'clientManagement'}, context_instance=RequestContext(request))

@login_required
def type_create(request):
	if request.method == 'POST':
		form = ComputerTypeForm(request.POST)
		if form.is_valid():
			t = form.save()
			messages.add_message(request, messages.SUCCESS, 'Der Computertyp "' + t.name + '" wurde erfolgreich erstellt.')
			return redirect('/pool/')
	else:
		form = ComputerTypeForm()

	return render_to_response('clientmanagement/type_form.html', {'form': form, 'action': 'Erstellen', 'active': 'clientManagement'}, context_instance=RequestContext(request))

@login_required
def key_create(request):
	if request.method == 'POST':
		form = WindowsKeyForm(request.POST)
		if form.is_valid():
			k = form.save()
			messages.add_message(request, messages.SUCCESS, 'Der Windows Key wurde erfolgreich erstellt.')
			return redirect('/pool/')
	else:
		form = WindowsKeyForm()

	return render_to_response('clientmanagement/key_form.html', {'form': form, 'action': 'Erstellen', 'active': 'clientManagement'}, context_instance=RequestContext(request))

@login_required
def key_edit(request, id):
	try:
		k = WindowsKey.objects.get(pk=id)
	except WindowsKey.DoesNotExist:
			return render_to_response('clientmanagement/404.html')

	if request.method == 'POST':
		form = WindowsKeyForm(request.POST, instance=k)
		if form.is_valid():
			k = form.save()
			messages.add_message(request, messages.SUCCESS, 'Der Windows Key wurde erfolgreich bearbeitet.')
			return redirect('/pool/')
	else:
		form = WindowsKeyForm(instance=k)

	return render_to_response('clientmanagement/key_form.html', {'form': form, 'action': 'Speichern', 'active': 'clientManagement'}, context_instance=RequestContext(request))

@login_required
def dhcp_config(request):
	computers = Computer.objects.filter(~Q(name='') and ~Q(ip_address=''))
	
	computer_list = []
	for c in computers:
		if re.search('([a-fA-F0-9]{2}[:|\-]?){6}', c.mac_address):
			computer_list.append(c)

	return render_to_response('clientmanagement/dhcp_config.txt', {'computers': computer_list}, content_type='text/plain', context_instance=RequestContext(request))

