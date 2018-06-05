from django.shortcuts import render_to_response, render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import auth
from django.core.context_processors import csrf
from django.contrib.auth.forms import UserCreationForm
from forms import *
from models import *
from django.template import RequestContext
from django.forms import models as forms_models
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from django.core.context_processors import csrf
from django.shortcuts import render
from reportlab.pdfgen import canvas
from django.utils import formats
from forum.profanity import *

# Create your views here.
def index(request):
    return HttpResponse("<h2>Hello World</h2>")

def add_csrf(request, ** kwargs):
    d = dict(user=request.user, ** kwargs)
    d.update(csrf(request))
    return d

def topic(request, topic_id):
    comments = Comment.objects.filter(topic=topic_id).order_by("created")
    topic = Topic.objects.get(pk=topic_id)
    provotes = topic.proPercent()
    convotes = 100-provotes
    if convotes == 0:
        convotes=5
    elif convotes == 100:
        convotes = 95
    seshString = "has_voted" + topic_id
    if seshString in request.session:
        hasVoted = request.session[seshString]
    else:
        hasVoted = 'False'
    seshString1 = "has_upvoted"+topic_id
    if seshString1 in request.session:
        hasUpvoted = request.session[seshString1]
    else:
        hasUpvoted = 'False'
    return render_to_response("topic.html", add_csrf(request, comments=comments , pk=topic_id, topic=topic, proVotes = provotes, convotes = convotes, hasVoted = hasVoted, hasUpvoted = hasUpvoted), context_instance=RequestContext(request))
 

def addpro(request, topic_id):
    topic = Topic.objects.get(pk=topic_id)
    topic.votesfor += 1
    topic.save()
    seshString = "has_voted" + topic_id
    request.session[seshString] = 'True'
    link = '/topics/' + topic_id + '/'
    return redirect(link)
 
def addcon(request, topic_id):
    topic = Topic.objects.get(pk=topic_id)
    topic.votesagainst += 1
    topic.save()
    seshString = "has_voted" + topic_id
    request.session[seshString] = 'True'
    link = '/topics/' + topic_id + '/'
    return redirect(link)

def upvote(request, topic_id, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    comment.score += 1
    comment.save()  
    seshString = "has_upvoted"+topic_id
    request.session[seshString] = 'True'
    link = '/topics/' + topic_id + '/'
    return redirect(link)


def pdf(request, topic_id):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
    # Create the PDF object, using the response object as its "file."
    topic = Topic.objects.get(pk=topic_id)
    p = canvas.Canvas(response)
    p.setLineWidth(.3)
    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.setFont('Helvetica', 20)
    p.drawString(70, 750, "TheBait")
    p.setFont('Helvetica', 12)
    p.drawString(70, 700, "Title: " + topic.title)
    p.line(70,695,500,695)
    p.drawString(70, 670, "Date Created: " + str(formats.date_format(topic.created, "SHORT_DATETIME_FORMAT")))
    p.line(70,665,500,665)
    p.drawString(70, 640, "Description:")
    p.line(70,635,500,635)
    p.drawString(70, 620, topic.description)
    p.drawString(70, 400, "Pros: " + topic.pros)
    p.drawString(70, 380, "Cons: " + topic.cons)
    p.line(70,395,500,395)
    p.showPage()
    p.save()
    return response


#@login_required
def post_reply(request, topic_id):
    form = CommentForm()
    topic = Topic.objects.get(pk=topic_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():

            comment = Comment()
            comment.topic = topic
            comment.body = form.cleaned_data['body']
            comment.body_html = form.cleaned_data['body']
            comment.user = request.user

            comment.save()

            return HttpResponseRedirect(reverse('topic-detail', args=(topic.id, )))

    return render_to_response('reply.html', {
            'form': form,
            'topic': topic,
        }, context_instance=RequestContext(request))

def deleteComment(request, topic_id, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    comment.delete()
    link = '/topics/' + topic_id + '/'
    return redirect(link)