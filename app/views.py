from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.contrib import messages

from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.urls import reverse

from app.dialogue.dialogue import *

def index(request):
	request.session.set_expiry(0)
        request.session['dialogue'] = Dialogue()
	return render(request, 'app/index.html')

@csrf_exempt
def query(request):
	request.session.set_expiry(0)

	'''View for responding to queries'''
	query = request.POST['query']
	
	dialogue = request.session['dialogue']
	(response, topic) = dialogue.getResponse(query) #Generate response to query
	template = ("<div data-toggle='popover' title='topic' data-trigger='hover' data-content='" + topic + "' data-placement='top'> <div class='panel-body received-msg'>" + response + "</div></div>" + "<a id=chatBody> </a>")
	request.session['dialogue'] = dialogue #Save updated session dialogue
	return HttpResponse(template, content_type='text/plain')
