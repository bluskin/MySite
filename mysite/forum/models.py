from __future__ import unicode_literals
from django.contrib import admin
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group



# Create your models here.



class Topic(models.Model):
    title = models.CharField(max_length=60)
    description = models.TextField(max_length=10000, blank=True, null=True)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True)
    pros = models.TextField()
    cons = models.TextField()
    votesfor = models.IntegerField()
    votesagainst = models.IntegerField()
    
    def num_comments(self):
        return self.Comment_set.count()

    def last_post(self):
        if self.Comment_set.count():
            return self.post_set.order_by("created")[0]
        
    def proPercent(self):
        if self.votesfor == 0 and self.votesagainst == 0:
            return 50
        else:
            numPro = self.votesfor
            numCon = self.votesagainst
           
            total = numPro + numCon
            proP = (numPro*100/total)
            return proP
 


    def __unicode__(self):
        return unicode(self.creator) + " - " + self.title


class Comment(models.Model):
    topic = models.ForeignKey(Topic, related_name='Topic', verbose_name=('Topic'))
    user = models.TextField()
    created = models.DateTimeField(('Created'), auto_now_add=True)
    updated = models.DateTimeField(('Updated'), blank=True, null=True)
    body = models.TextField()
    score = models.IntegerField(default = 0)

    class Meta:
        ordering = ['created']
        get_latest_by = 'created'
        verbose_name = ('Comment')
        verbose_name_plural = ('comments')

    def save(self, *args, **kwargs):
        super(Comment, self).save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        super(Comment, self).delete(*args, **kwargs)

    def __unicode__(self):
        return unicode(self.body)