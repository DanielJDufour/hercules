from django.conf import settings
from django.db import models
#from django.contrib.gis.db import models as geomodels
from django.db.models.signals import m2m_changed, post_save
from django.contrib.auth.models import User
import re, requests
from bs4 import BeautifulSoup

class Donation(models.Model):
    donor = models.ForeignKey('Donor', null=True, blank=True)
    amount = models.DecimalField(max_digits=100, default=0.00,decimal_places=2)
    recipient = models.ManyToManyField('Organization')

class Donor(models.Model):
    user = models.ForeignKey(User, unique=True, null=True)
    donated = models.DecimalField(max_digits=100, default=0.00,decimal_places=2)

class Link(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    def __str__(self):
        return self.title
    class Meta:
        ordering = ['title']

class Location(models.Model):
    name = models.CharField(max_length=200)
#    coords = geomodels.PointField()
#    polygon = geomodels.PolygonField()

    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']
 

class Membership(models.Model):
    organization = models.ForeignKey('Organization')
    person = models.ForeignKey('Person')
    position = models.CharField(max_length=200, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)


class Organization(models.Model):
    bricked = models.BooleanField(default=False)
    hidden = models.BooleanField(default=True)
    name = models.CharField(max_length=200)
    abbreviation = models.CharField(max_length=200, blank=True, null=True)
    slug = models.SlugField(unique=True)
    logo = models.ImageField(upload_to="images/logos", blank=True, null=True)
    entry_created = models.DateTimeField(auto_now_add=True)
    organization_created = models.DateField(null=True, blank=True)
    members = models.ManyToManyField('Person', through='Membership')
    links = models.ManyToManyField('Link', blank=True)
    projects = models.ManyToManyField('Project', blank=True)
    partners = models.ManyToManyField('Organization', blank=True)
    facebook = models.CharField(max_length=200, null=True, blank=True)
    twitter = models.CharField(max_length=200, null=True, blank=True)
    linkedin = models.CharField(max_length=200, null=True, blank=True) 
    wiki = models.CharField(max_length=200, null=True, blank=True)


    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']

class Person(models.Model):
    user = models.OneToOneField(User, blank=True, null=True)
    notable = models.NullBooleanField(blank=True, null=True, default=False)
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    pic = models.ImageField(upload_to="images/biopics", blank=True, null=True)
    story = models.TextField(null=True, blank=True)
    hometown = models.CharField(max_length=200, null=True, blank=True)
    facebook_url = models.URLField(max_length=200, null=True, blank=True)
    facebook_title = models.CharField(max_length=200, null=True, blank=True)
    twitter = models.CharField(max_length=200, null=True, blank=True)
    wiki_title = models.CharField(max_length=200, null=True, blank=True)
    wiki_url = models.URLField(max_length=200, null=True, blank=True)
    def update(self):
        self.updateFacebook()
        self.updateWiki()
    def updateFacebook(self):
        print "starting updateWiki"
        print "facebook_url is", self.facebook_url
        if self.facebook_url == "":
            self.facebook_title = ""
        else:
            self.facebook_title = BeautifulSoup(requests.get(self.facebook_url).content).title.string.split(" -")[0].strip() 
            self.save()
    def updateWiki(self):
        print "starting updateWiki"

        print "wiki_url is", self.wiki_url
        if self.wiki_url == "":
            self.wiki_title = ""
        else:
            self.wiki_title = re.search('(?<=wiki\/)\w+', self.wiki_url).group(0)
            self.save()
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']
   
class Privacy(models.Model):
    hidden = models.BooleanField(default=True)

class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    steps = models.ManyToManyField('Step', blank=True)

    def __str__(self):
        return self.title
    class Meta:
        ordering = ['title']

class Step(models.Model):
    name = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.name
    
class Video(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    embed = models.TextField(default="",null=True,blank=True)
    def __str__(self):
        return self.title
    class Meta:
        ordering = ['title']

class TeamMember(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    picture = models.ImageField(upload_to="images", null=True, blank=True, default=settings.STATIC_URL+"skyshaker/img/user/default.jpg")
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']

def updatePartners(sender, instance, **kwargs):
    print "updating partners"    
    #instance.save()
    #instance.partners.remove()
    #instance.updatePartners(instance)
    #instance.save()

def updateVideoEmbed(sender, instance, **kwargs):
    instance_url = str(instance.url)
    if 'youtube' in instance_url:
        idOfYoutubeVideo = re.search('(?<=v=)\w+', instance_url).group(0)
        instance.embed = '<iframe width="100%" height="315" src="//www.youtube.com/embed/' + idOfYoutubeVideo + '" frameborder="0" allowfullscreen></iframe>'
    elif 'vimeo' in instance.url:
        idOfVimeoVideo = re.search('(?<=com/)\w+', instance_url).group(0)
        instance.embed = '<iframe src="//player.vimeo.com/video/' + idOfVimeoVideo + '" width="500" height="281" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>'
    post_save.disconnect(updateVideoEmbed, sender=Video)
    instance.save()
    post_save.connect(updateVideoEmbed, sender=Video)


m2m_changed.connect(updatePartners, sender=Organization.projects.through)
post_save.connect(updateVideoEmbed, sender=Video)
